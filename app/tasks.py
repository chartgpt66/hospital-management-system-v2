from celery import Celery
from celery.schedules import crontab
from flask import current_app
from flask_mail import Message
from app import mail, db
from app.models import Appointment, Doctor, Patient, Treatment
from datetime import date, datetime, timedelta
import csv
import os
from io import StringIO

# Initialize Celery
celery = Celery('tasks')

def init_celery(app):
    """Initialize Celery with Flask app context"""
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone='UTC',
        enable_utc=True,
    )
    
    # Configure beat schedule
    celery.conf.beat_schedule = {
        'send-daily-reminders': {
            'task': 'app.tasks.send_daily_reminders',
            'schedule': crontab(hour=8, minute=0),  # 8 AM daily
        },
        'send-monthly-reports': {
            'task': 'app.tasks.send_monthly_reports',
            'schedule': crontab(day_of_month=1, hour=9, minute=0),  # 1st of month at 9 AM
        },
    }
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

@celery.task(name='app.tasks.send_daily_reminders')
def send_daily_reminders():
    """Send daily appointment reminders to patients"""
    today = date.today()
    
    # Get all appointments for today
    appointments = Appointment.query.filter_by(
        appointment_date=today,
        status='booked'
    ).all()
    
    sent_count = 0
    
    for apt in appointments:
        try:
            patient_email = apt.patient.user.email
            doctor_name = apt.doctor.full_name
            appointment_time = apt.appointment_time.strftime('%I:%M %p')
            
            msg = Message(
                subject='Appointment Reminder - Hospital Management System',
                recipients=[patient_email],
                body=f"""
Dear {apt.patient.full_name},

This is a reminder for your appointment today:

Doctor: {doctor_name}
Specialization: {apt.doctor.specialization.name}
Time: {appointment_time}
Date: {today.strftime('%B %d, %Y')}

Please arrive 10 minutes early for registration.

Best regards,
Hospital Management System
                """
            )
            
            mail.send(msg)
            sent_count += 1
            
        except Exception as e:
            current_app.logger.error(f"Failed to send reminder to {patient_email}: {str(e)}")
    
    return f"Sent {sent_count} reminders"

@celery.task(name='app.tasks.send_monthly_reports')
def send_monthly_reports():
    """Send monthly activity reports to doctors"""
    # Get previous month's date range
    today = date.today()
    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    
    doctors = Doctor.query.filter_by(is_available=True).all()
    
    sent_count = 0
    
    for doctor in doctors:
        try:
            # Get appointments for previous month
            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.appointment_date.between(first_day_previous_month, last_day_previous_month)
            ).all()
            
            if not appointments:
                continue
            
            # Generate report
            total_appointments = len(appointments)
            completed = len([a for a in appointments if a.status == 'completed'])
            cancelled = len([a for a in appointments if a.status == 'cancelled'])
            
            # Create HTML report
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .header {{ background-color: #4CAF50; color: white; padding: 20px; }}
                    .content {{ padding: 20px; }}
                    .stats {{ background-color: #f2f2f2; padding: 15px; margin: 10px 0; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #4CAF50; color: white; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Monthly Activity Report</h1>
                    <p>{first_day_previous_month.strftime('%B %Y')}</p>
                </div>
                <div class="content">
                    <h2>Dr. {doctor.full_name}</h2>
                    <p>Specialization: {doctor.specialization.name}</p>
                    
                    <div class="stats">
                        <h3>Summary Statistics</h3>
                        <p><strong>Total Appointments:</strong> {total_appointments}</p>
                        <p><strong>Completed:</strong> {completed}</p>
                        <p><strong>Cancelled:</strong> {cancelled}</p>
                    </div>
                    
                    <h3>Appointment Details</h3>
                    <table>
                        <tr>
                            <th>Date</th>
                            <th>Patient</th>
                            <th>Status</th>
                            <th>Diagnosis</th>
                        </tr>
            """
            
            for apt in appointments:
                diagnosis = apt.treatment.diagnosis if apt.treatment else 'N/A'
                html_body += f"""
                        <tr>
                            <td>{apt.appointment_date.strftime('%Y-%m-%d')}</td>
                            <td>{apt.patient.full_name}</td>
                            <td>{apt.status}</td>
                            <td>{diagnosis}</td>
                        </tr>
                """
            
            html_body += """
                    </table>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=f'Monthly Activity Report - {first_day_previous_month.strftime("%B %Y")}',
                recipients=[doctor.user.email],
                html=html_body
            )
            
            mail.send(msg)
            sent_count += 1
            
        except Exception as e:
            current_app.logger.error(f"Failed to send report to {doctor.user.email}: {str(e)}")
    
    return f"Sent {sent_count} monthly reports"

@celery.task(name='app.tasks.export_treatment_csv', bind=True)
def export_treatment_csv(self, patient_id, email):
    """Export patient treatment history as CSV"""
    try:
        self.update_state(state='PROGRESS', meta={'status': 'Fetching treatment data...'})
        
        patient = Patient.query.get(patient_id)
        if not patient:
            return {'status': 'error', 'message': 'Patient not found'}
        
        # Get all completed appointments with treatments
        appointments = Appointment.query.filter_by(
            patient_id=patient_id,
            status='completed'
        ).order_by(Appointment.appointment_date.desc()).all()
        
        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Patient ID',
            'Patient Name',
            'Doctor Name',
            'Specialization',
            'Appointment Date',
            'Diagnosis',
            'Prescription',
            'Treatment Notes',
            'Next Visit Date'
        ])
        
        # Write data
        for apt in appointments:
            if apt.treatment:
                writer.writerow([
                    patient.id,
                    patient.full_name,
                    apt.doctor.full_name,
                    apt.doctor.specialization.name,
                    apt.appointment_date.strftime('%Y-%m-%d'),
                    apt.treatment.diagnosis,
                    apt.treatment.prescription or 'N/A',
                    apt.treatment.notes or 'N/A',
                    apt.treatment.next_visit_date.strftime('%Y-%m-%d') if apt.treatment.next_visit_date else 'N/A'
                ])
        
        csv_content = output.getvalue()
        output.close()
        
        self.update_state(state='PROGRESS', meta={'status': 'Sending email...'})
        
        # Send email with CSV attachment
        msg = Message(
            subject='Your Treatment History Export',
            recipients=[email],
            body=f"""
Dear {patient.full_name},

Your treatment history export is ready. Please find the CSV file attached.

This file contains all your completed appointments and treatment details.

Best regards,
Hospital Management System
            """
        )
        
        msg.attach(
            f'treatment_history_{patient_id}_{datetime.now().strftime("%Y%m%d")}.csv',
            'text/csv',
            csv_content
        )
        
        mail.send(msg)
        
        return {
            'status': 'success',
            'message': 'CSV exported and sent via email',
            'records': len(appointments)
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
