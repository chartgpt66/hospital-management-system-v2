from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Patient, Doctor, Appointment, Specialization, DoctorAvailability, Treatment
from app.utils.decorators import patient_required
from app.utils.cache import cached
from datetime import datetime, date, timedelta

bp = Blueprint('patient', __name__, url_prefix='/patient')

@bp.route('/dashboard', methods=['GET'])
@login_required
@patient_required
def dashboard():
    """Get patient dashboard data"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    today = date.today()
    
    stats = {
        'upcoming_appointments': Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.appointment_date >= today,
            Appointment.status == 'booked'
        ).count(),
        'total_appointments': Appointment.query.filter_by(patient_id=patient.id).count(),
        'completed_appointments': Appointment.query.filter_by(
            patient_id=patient.id,
            status='completed'
        ).count()
    }
    
    return jsonify(stats), 200

@bp.route('/profile', methods=['GET'])
@login_required
@patient_required
def get_profile():
    """Get patient profile"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    profile = {
        'id': patient.id,
        'full_name': patient.full_name,
        'email': current_user.email,
        'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        'gender': patient.gender,
        'contact_number': patient.contact_number,
        'address': patient.address,
        'medical_history': patient.medical_history
    }
    
    return jsonify(profile), 200

@bp.route('/profile', methods=['PUT'])
@login_required
@patient_required
def update_profile():
    """Update patient profile"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    try:
        if 'full_name' in data:
            patient.full_name = data['full_name']
        if 'date_of_birth' in data:
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        if 'gender' in data:
            patient.gender = data['gender']
        if 'contact_number' in data:
            patient.contact_number = data['contact_number']
        if 'address' in data:
            patient.address = data['address']
        if 'medical_history' in data:
            patient.medical_history = data['medical_history']
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/specializations', methods=['GET'])
@login_required
@patient_required
def get_specializations():
    """Get all specializations"""
    specializations = Specialization.query.all()
    
    spec_list = []
    for spec in specializations:
        spec_list.append({
            'id': spec.id,
            'name': spec.name,
            'description': spec.description,
            'doctors_count': spec.doctors_count
        })
    
    return jsonify(spec_list), 200

@bp.route('/doctors', methods=['GET'])
@login_required
@patient_required
def get_doctors():
    """Get doctors by specialization"""
    specialization_id = request.args.get('specialization_id', type=int)
    
    query = Doctor.query.filter_by(is_available=True)
    
    if specialization_id:
        query = query.filter_by(specialization_id=specialization_id)
    
    doctors = query.all()
    
    doctors_list = []
    for doctor in doctors:
        doctors_list.append({
            'id': doctor.id,
            'full_name': doctor.full_name,
            'specialization': doctor.specialization.name,
            'qualification': doctor.qualification,
            'experience_years': doctor.experience_years,
            'consultation_fee': doctor.consultation_fee
        })
    
    return jsonify(doctors_list), 200

@bp.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
@login_required
@patient_required
def get_doctor_availability(doctor_id):
    """Get doctor's availability for next 7 days"""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    today = date.today()
    week_end = today + timedelta(days=7)
    
    availability = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date.between(today, week_end),
        DoctorAvailability.is_booked == False
    ).order_by(DoctorAvailability.date, DoctorAvailability.start_time).all()
    
    availability_list = []
    for slot in availability:
        availability_list.append({
            'id': slot.id,
            'date': slot.date.isoformat(),
            'start_time': slot.start_time.isoformat(),
            'end_time': slot.end_time.isoformat()
        })
    
    return jsonify(availability_list), 200

@bp.route('/appointments', methods=['POST'])
@login_required
@patient_required
def book_appointment():
    """Book an appointment"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    required_fields = ['doctor_id', 'appointment_date', 'appointment_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(data['appointment_time'], '%H:%M').time()
        
        # Check if slot is already booked
        existing = Appointment.query.filter_by(
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='booked'
        ).first()
        
        if existing:
            return jsonify({'error': 'This time slot is already booked'}), 400
        
        # Create appointment
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=data.get('reason'),
            status='booked'
        )
        db.session.add(appointment)
        
        # Mark availability slot as booked
        availability = DoctorAvailability.query.filter_by(
            doctor_id=data['doctor_id'],
            date=appointment_date
        ).filter(
            DoctorAvailability.start_time <= appointment_time,
            DoctorAvailability.end_time > appointment_time
        ).first()
        
        if availability:
            availability.is_booked = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Appointment booked successfully',
            'appointment_id': appointment.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments', methods=['GET'])
@login_required
@patient_required
def get_appointments():
    """Get patient's appointments"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    status = request.args.get('status')
    
    query = Appointment.query.filter_by(patient_id=patient.id)
    
    if status:
        query = query.filter_by(status=status)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    
    appointments_list = []
    for apt in appointments:
        apt_data = {
            'id': apt.id,
            'doctor_name': apt.doctor.full_name,
            'specialization': apt.doctor.specialization.name,
            'appointment_date': apt.appointment_date.isoformat(),
            'appointment_time': apt.appointment_time.isoformat(),
            'status': apt.status,
            'reason': apt.reason
        }
        
        if apt.treatment:
            apt_data['treatment'] = {
                'diagnosis': apt.treatment.diagnosis,
                'prescription': apt.treatment.prescription,
                'notes': apt.treatment.notes,
                'next_visit_date': apt.treatment.next_visit_date.isoformat() if apt.treatment.next_visit_date else None
            }
        
        appointments_list.append(apt_data)
    
    return jsonify(appointments_list), 200

@bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@patient_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    appointment = Appointment.query.filter_by(id=appointment_id, patient_id=patient.id).first_or_404()
    
    if appointment.status != 'booked':
        return jsonify({'error': 'Only booked appointments can be cancelled'}), 400
    
    try:
        appointment.status = 'cancelled'
        
        # Free up the availability slot
        availability = DoctorAvailability.query.filter_by(
            doctor_id=appointment.doctor_id,
            date=appointment.appointment_date
        ).filter(
            DoctorAvailability.start_time <= appointment.appointment_time,
            DoctorAvailability.end_time > appointment.appointment_time
        ).first()
        
        if availability:
            availability.is_booked = False
        
        db.session.commit()
        
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/treatment-history', methods=['GET'])
@login_required
@patient_required
def get_treatment_history():
    """Get patient's complete treatment history"""
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status='completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    history = []
    for apt in appointments:
        if apt.treatment:
            history.append({
                'appointment_id': apt.id,
                'doctor_name': apt.doctor.full_name,
                'specialization': apt.doctor.specialization.name,
                'appointment_date': apt.appointment_date.isoformat(),
                'diagnosis': apt.treatment.diagnosis,
                'prescription': apt.treatment.prescription,
                'notes': apt.treatment.notes,
                'next_visit_date': apt.treatment.next_visit_date.isoformat() if apt.treatment.next_visit_date else None
            })
    
    return jsonify(history), 200
