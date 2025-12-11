from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, Patient
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Patient registration endpoint"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'full_name', 'contact_number']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    try:
        # Create user account
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            role='patient',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        # Create patient profile
        patient = Patient(
            user_id=user.id,
            full_name=data['full_name'],
            date_of_birth=datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            contact_number=data['contact_number'],
            address=data.get('address'),
            medical_history=data.get('medical_history')
        )
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login endpoint for all users"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    login_user(user, remember=data.get('remember', False))
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout endpoint"""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user details"""
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
        'is_active': current_user.is_active
    }
    
    if current_user.role == 'patient' and current_user.patient:
        user_data['profile'] = {
            'full_name': current_user.patient.full_name,
            'contact_number': current_user.patient.contact_number,
            'date_of_birth': current_user.patient.date_of_birth.isoformat() if current_user.patient.date_of_birth else None,
            'gender': current_user.patient.gender,
            'address': current_user.patient.address
        }
    elif current_user.role == 'doctor' and current_user.doctor:
        user_data['profile'] = {
            'full_name': current_user.doctor.full_name,
            'specialization': current_user.doctor.specialization.name,
            'qualification': current_user.doctor.qualification,
            'experience_years': current_user.doctor.experience_years
        }
    
    return jsonify(user_data), 200
