from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Doctor, Appointment, Treatment, DoctorAvailability
from app.utils.decorators import doctor_required
from datetime import datetime, date, time, timedelta

bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@bp.route('/dashboard', methods=['GET'])
@login_required
@doctor_required
def dashboard():
    """Get doctor dashboard statistics"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    today = date.today()
    week_end = today + timedelta(days=7)
    
    stats = {
        'upcoming_appointments_today': Appointment.query.filter_by(
            doctor_id=doctor.id,
            appointment_date=today,
            status='booked'
        ).count(),
        'upcoming_appointments_week': Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date.between(today, week_end),
            Appointment.status == 'booked'
        ).count(),
        'total_patients': db.session.query(Appointment.patient_id).filter_by(
            doctor_id=doctor.id
        ).distinct().count(),
        'completed_appointments': Appointment.query.filter_by(
            doctor_id=doctor.id,
            status='completed'
        ).count()
    }
    
    return jsonify(stats), 200

@bp.route('/appointments', methods=['GET'])
@login_required
@doctor_required
def get_appointments():
    """Get doctor's appointments"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    status = request.args.get('status')
    date_filter = request.args.get('date')
    
    query = Appointment.query.filter_by(doctor_id=doctor.id)
    
    if status:
        query = query.filter_by(status=status)
    
    if date_filter:
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        query = query.filter_by(appointment_date=filter_date)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    
    appointments_list = []
    for apt in appointments:
        apt_data = {
            'id': apt.id,
            'patient_id': apt.patient_id,
            'patient_name': apt.patient.full_name,
            'patient_contact': apt.patient.contact_number,
            'appointment_date': apt.appointment_date.isoformat(),
            'appointment_time': apt.appointment_time.isoformat(),
            'status': apt.status,
            'reason': apt.reason
        }
        
        if apt.treatment:
            apt_data['treatment'] = {
                'diagnosis': apt.treatment.diagnosis,
                'prescription': apt.treatment.prescription,
                'notes': apt.treatment.notes
            }
        
        appointments_list.append(apt_data)
    
    return jsonify(appointments_list), 200

@bp.route('/appointments/<int:appointment_id>/complete', methods=['POST'])
@login_required
@doctor_required
def complete_appointment(appointment_id):
    """Mark appointment as completed and add treatment"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    appointment = Appointment.query.filter_by(id=appointment_id, doctor_id=doctor.id).first_or_404()
    
    if appointment.status != 'booked':
        return jsonify({'error': 'Only booked appointments can be completed'}), 400
    
    data = request.get_json()
    
    if not data.get('diagnosis'):
        return jsonify({'error': 'Diagnosis is required'}), 400
    
    try:
        # Update appointment status
        appointment.status = 'completed'
        
        # Create treatment record
        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=data['diagnosis'],
            prescription=data.get('prescription'),
            notes=data.get('notes'),
            next_visit_date=datetime.strptime(data['next_visit_date'], '%Y-%m-%d').date() if data.get('next_visit_date') else None
        )
        db.session.add(treatment)
        db.session.commit()
        
        return jsonify({'message': 'Appointment completed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@doctor_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    appointment = Appointment.query.filter_by(id=appointment_id, doctor_id=doctor.id).first_or_404()
    
    if appointment.status != 'booked':
        return jsonify({'error': 'Only booked appointments can be cancelled'}), 400
    
    try:
        appointment.status = 'cancelled'
        db.session.commit()
        
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/patients/<int:patient_id>/history', methods=['GET'])
@login_required
@doctor_required
def get_patient_history(patient_id):
    """Get patient's treatment history"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get all completed appointments for this patient with this doctor
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor.id,
        status='completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    history = []
    for apt in appointments:
        if apt.treatment:
            history.append({
                'appointment_id': apt.id,
                'appointment_date': apt.appointment_date.isoformat(),
                'diagnosis': apt.treatment.diagnosis,
                'prescription': apt.treatment.prescription,
                'notes': apt.treatment.notes,
                'next_visit_date': apt.treatment.next_visit_date.isoformat() if apt.treatment.next_visit_date else None
            })
    
    return jsonify(history), 200

@bp.route('/availability', methods=['GET'])
@login_required
@doctor_required
def get_availability():
    """Get doctor's availability schedule"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    
    today = date.today()
    week_end = today + timedelta(days=7)
    
    availability = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor.id,
        DoctorAvailability.date.between(today, week_end)
    ).order_by(DoctorAvailability.date, DoctorAvailability.start_time).all()
    
    availability_list = []
    for slot in availability:
        availability_list.append({
            'id': slot.id,
            'date': slot.date.isoformat(),
            'start_time': slot.start_time.isoformat(),
            'end_time': slot.end_time.isoformat(),
            'is_booked': slot.is_booked
        })
    
    return jsonify(availability_list), 200

@bp.route('/availability', methods=['POST'])
@login_required
@doctor_required
def add_availability():
    """Add availability slot"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    required_fields = ['date', 'start_time', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        availability = DoctorAvailability(
            doctor_id=doctor.id,
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            is_booked=False
        )
        db.session.add(availability)
        db.session.commit()
        
        return jsonify({'message': 'Availability added successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/availability/<int:slot_id>', methods=['DELETE'])
@login_required
@doctor_required
def delete_availability(slot_id):
    """Delete availability slot"""
    doctor = Doctor.query.filter_by(user_id=current_user.id).first_or_404()
    slot = DoctorAvailability.query.filter_by(id=slot_id, doctor_id=doctor.id).first_or_404()
    
    if slot.is_booked:
        return jsonify({'error': 'Cannot delete booked slot'}), 400
    
    try:
        db.session.delete(slot)
        db.session.commit()
        
        return jsonify({'message': 'Availability slot deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
