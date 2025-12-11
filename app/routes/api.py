from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models import Patient, Appointment, Treatment
from app.tasks import export_treatment_csv
import os

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/export/treatments', methods=['POST'])
@login_required
def export_treatments():
    """Trigger async CSV export of patient treatments"""
    if current_user.role != 'patient':
        return jsonify({'error': 'Only patients can export their treatment history'}), 403
    
    patient = Patient.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Trigger async task
    task = export_treatment_csv.delay(patient.id, current_user.email)
    
    return jsonify({
        'message': 'Export started. You will receive an email when ready.',
        'task_id': task.id
    }), 202

@bp.route('/export/status/<task_id>', methods=['GET'])
@login_required
def export_status(task_id):
    """Check status of export task"""
    from app.tasks import celery
    task = celery.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is waiting to be processed'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'status': task.info.get('status', '')
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'status': 'Export completed',
            'result': task.info
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    
    return jsonify(response), 200

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Hospital Management System API is running'
    }), 200
