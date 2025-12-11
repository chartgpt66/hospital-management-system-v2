from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db, bcrypt
from app.models import User, Doctor, Patient, Appointment, Specialization, Treatment
from app.utils.decorators import admin_required
from app.utils.cache import invalidate_pattern
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Get admin dashboard statistics"""
    stats = {
        'total_doctors': Doctor.query.filter_by(is_available=True).count(),
        'total_patients': Patient.query.count(),
        'total_appointments': Appointment.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='booked').count(),
        'completed_appointments': Appointment.query.filter_by(status='completed').count(),
        'cancelled_appointments': Appointment.query.filter_by(status='cancelled').count(),
        'total_specializations': Specialization.query.count()
    }
    return jsonify(stats), 200

@bp.route('/doctors', methods=['GET'])
@login_required
@admin_required
def get_doctors():
    """Get all doctors"""
    doctors = Doctor.query.all()
    doctors_list = []
    
    for doctor in doctors:
        doctors_list.append({
            'id': doctor.id,
            'user_id': doctor.user_id,
            'full_name': doctor.full_name,
            'specialization': doctor.specialization.name,
            'qualification': doctor.qualification,
            'experience_years': doctor.experience_years,
            'consultation_fee': doctor.consultation_fee,
            'is_available': doctor.is_available,
            'email': doctor.user.email,
            'username': doctor.user.username
        })
    
    return jsonify(doctors_list), 200

@bp.route('/doctors', methods=['POST'])
@login_required
@admin_required
def add_doctor():
    """Add new doctor"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'full_name', 'specialization_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if username or email exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    try:
        # Create user account
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            role='doctor',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        # Create doctor profile
        doctor = Doctor(
            user_id=user.id,
            full_name=data['full_name'],
            specialization_id=data['specialization_id'],
            qualification=data.get('qualification'),
            experience_years=data.get('experience_years', 0),
            consultation_fee=data.get('consultation_fee', 0),
            is_available=True
        )
        db.session.add(doctor)
        db.session.commit()
        
        # Invalidate cache
        invalidate_pattern('doctors:*')
        
        return jsonify({
            'message': 'Doctor added successfully',
            'doctor_id': doctor.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
@login_required
@admin_required
def update_doctor(doctor_id):
    """Update doctor details"""
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json()
    
    try:
        if 'full_name' in data:
            doctor.full_name = data['full_name']
        if 'specialization_id' in data:
            doctor.specialization_id = data['specialization_id']
        if 'qualification' in data:
            doctor.qualification = data['qualification']
        if 'experience_years' in data:
            doctor.experience_years = data['experience_years']
        if 'consultation_fee' in data:
            doctor.consultation_fee = data['consultation_fee']
        if 'is_available' in data:
            doctor.is_available = data['is_available']
        
        db.session.commit()
        
        # Invalidate cache
        invalidate_pattern('doctors:*')
        
        return jsonify({'message': 'Doctor updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_doctor(doctor_id):
    """Delete/deactivate doctor"""
    doctor = Doctor.query.get_or_404(doctor_id)
    
    try:
        # Deactivate user account instead of deleting
        doctor.user.is_active = False
        doctor.is_available = False
        db.session.commit()
        
        # Invalidate cache
        invalidate_pattern('doctors:*')
        
        return jsonify({'message': 'Doctor deactivated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/patients', methods=['GET'])
@login_required
@admin_required
def get_patients():
    """Get all patients"""
    patients = Patient.query.all()
    patients_list = []
    
    for patient in patients:
        patients_list.append({
            'id': patient.id,
            'user_id': patient.user_id,
            'full_name': patient.full_name,
            'email': patient.user.email,
            'contact_number': patient.contact_number,
            'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            'gender': patient.gender,
            'is_active': patient.user.is_active
        })
    
    return jsonify(patients_list), 200

@bp.route('/patients/<int:patient_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_patient(patient_id):
    """Delete/deactivate patient"""
    patient = Patient.query.get_or_404(patient_id)
    
    try:
        # Deactivate user account
        patient.user.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Patient deactivated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/appointments', methods=['GET'])
@login_required
@admin_required
def get_all_appointments():
    """Get all appointments"""
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    appointments_list = []
    
    for apt in appointments:
        appointments_list.append({
            'id': apt.id,
            'patient_name': apt.patient.full_name,
            'doctor_name': apt.doctor.full_name,
            'specialization': apt.doctor.specialization.name,
            'appointment_date': apt.appointment_date.isoformat(),
            'appointment_time': apt.appointment_time.isoformat(),
            'status': apt.status,
            'reason': apt.reason
        })
    
    return jsonify(appointments_list), 200

@bp.route('/search/doctors', methods=['GET'])
@login_required
@admin_required
def search_doctors():
    """Search doctors by name or specialization"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    doctors = Doctor.query.join(Specialization).filter(
        db.or_(
            Doctor.full_name.ilike(f'%{query}%'),
            Specialization.name.ilike(f'%{query}%')
        )
    ).all()
    
    results = []
    for doctor in doctors:
        results.append({
            'id': doctor.id,
            'full_name': doctor.full_name,
            'specialization': doctor.specialization.name,
            'qualification': doctor.qualification,
            'experience_years': doctor.experience_years,
            'is_available': doctor.is_available
        })
    
    return jsonify(results), 200

@bp.route('/search/patients', methods=['GET'])
@login_required
@admin_required
def search_patients():
    """Search patients by name or contact"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    patients = Patient.query.filter(
        db.or_(
            Patient.full_name.ilike(f'%{query}%'),
            Patient.contact_number.ilike(f'%{query}%')
        )
    ).all()
    
    results = []
    for patient in patients:
        results.append({
            'id': patient.id,
            'full_name': patient.full_name,
            'contact_number': patient.contact_number,
            'email': patient.user.email,
            'is_active': patient.user.is_active
        })
    
    return jsonify(results), 200
