from datetime import datetime, date, time, timedelta
from app import db, bcrypt
from app.models import User, Patient, Doctor, Specialization, DoctorAvailability

def create_admin_user():
    """Create default admin user if not exists"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@hospital.com',
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created successfully (username: admin, password: admin123)")
    else:
        print("✓ Admin user already exists")

def create_sample_data():
    """Create sample specializations and doctors for testing"""
    # Check if data already exists
    if Specialization.query.count() > 0:
        print("✓ Sample data already exists")
        return
    
    # Create specializations
    specializations = [
        Specialization(name='Cardiology', description='Heart and cardiovascular system'),
        Specialization(name='Neurology', description='Brain and nervous system'),
        Specialization(name='Orthopedics', description='Bones, joints, and muscles'),
        Specialization(name='Pediatrics', description='Children healthcare'),
        Specialization(name='Dermatology', description='Skin, hair, and nails'),
        Specialization(name='General Medicine', description='General health and wellness'),
    ]
    
    for spec in specializations:
        db.session.add(spec)
    
    db.session.commit()
    
    # Create sample doctors
    doctors_data = [
        {
            'username': 'dr.sharma',
            'email': 'sharma@hospital.com',
            'full_name': 'Dr. Rajesh Sharma',
            'specialization': 'Cardiology',
            'qualification': 'MBBS, MD (Cardiology)',
            'experience': 15,
            'fee': 1000
        },
        {
            'username': 'dr.patel',
            'email': 'patel@hospital.com',
            'full_name': 'Dr. Priya Patel',
            'specialization': 'Neurology',
            'qualification': 'MBBS, DM (Neurology)',
            'experience': 12,
            'fee': 1200
        },
        {
            'username': 'dr.kumar',
            'email': 'kumar@hospital.com',
            'full_name': 'Dr. Amit Kumar',
            'specialization': 'Orthopedics',
            'qualification': 'MBBS, MS (Orthopedics)',
            'experience': 10,
            'fee': 900
        },
    ]
    
    for doc_data in doctors_data:
        # Create user account
        user = User(
            username=doc_data['username'],
            email=doc_data['email'],
            password_hash=bcrypt.generate_password_hash('doctor123').decode('utf-8'),
            role='doctor',
            is_active=True
        )
        db.session.add(user)
        db.session.flush()
        
        # Get specialization
        spec = Specialization.query.filter_by(name=doc_data['specialization']).first()
        
        # Create doctor profile
        doctor = Doctor(
            user_id=user.id,
            full_name=doc_data['full_name'],
            specialization_id=spec.id,
            qualification=doc_data['qualification'],
            experience_years=doc_data['experience'],
            consultation_fee=doc_data['fee'],
            is_available=True
        )
        db.session.add(doctor)
        db.session.flush()
        
        # Create availability for next 7 days
        for i in range(7):
            availability_date = date.today() + timedelta(days=i)
            
            # Morning slot
            morning_slot = DoctorAvailability(
                doctor_id=doctor.id,
                date=availability_date,
                start_time=time(9, 0),
                end_time=time(12, 0),
                is_booked=False
            )
            db.session.add(morning_slot)
            
            # Evening slot
            evening_slot = DoctorAvailability(
                doctor_id=doctor.id,
                date=availability_date,
                start_time=time(14, 0),
                end_time=time(17, 0),
                is_booked=False
            )
            db.session.add(evening_slot)
    
    db.session.commit()
    print("✓ Sample specializations and doctors created successfully")
    print("  Sample doctor credentials: username='dr.sharma', password='doctor123'")
