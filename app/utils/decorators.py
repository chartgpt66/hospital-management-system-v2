from functools import wraps
from flask import jsonify, redirect, url_for, flash
from flask_login import current_user

def role_required(role):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            
            if current_user.role != role:
                return jsonify({'error': f'Access denied. {role.capitalize()} role required'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator for admin-only routes"""
    return role_required('admin')(f)

def doctor_required(f):
    """Decorator for doctor-only routes"""
    return role_required('doctor')(f)

def patient_required(f):
    """Decorator for patient-only routes"""
    return role_required('patient')(f)
