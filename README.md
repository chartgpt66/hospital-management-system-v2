# Hospital Management System V2

A comprehensive web-based Hospital Management System built with Flask, Vue.js, Redis, and Celery. Supports three user roles: Admin, Doctor, and Patient with complete appointment management, treatment tracking, and automated background jobs.

## 🚀 Features

### Admin Features
- Dashboard with comprehensive statistics
- Add, update, and manage doctor profiles
- View and manage all appointments
- Search doctors by name or specialization
- Search patients by name or contact
- Deactivate doctors and patients

### Doctor Features
- Dashboard showing upcoming appointments
- View assigned appointments
- Mark appointments as completed
- Add diagnosis, prescriptions, and treatment notes
- View patient treatment history
- Manage availability schedule (7-day view)

### Patient Features
- Register and login
- Browse specializations/departments
- Search doctors by specialization
- View doctor availability (7 days ahead)
- Book, reschedule, and cancel appointments
- View appointment history
- Access complete treatment history
- Export treatment history as CSV

### Background Jobs
1. **Daily Reminders** - Sends email reminders to patients with appointments
2. **Monthly Reports** - Generates and emails monthly activity reports to doctors
3. **CSV Export** - Async export of patient treatment history

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Vue.js 3 (CDN)
- **Database**: SQLite
- **Caching**: Redis
- **Task Queue**: Celery + Redis
- **Styling**: Bootstrap 5
- **Email**: Flask-Mail

## 📋 Prerequisites

- Python 3.8+
- Redis Server
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/chartgpt66/hospital-management-system-v2.git
cd hospital-management-system-v2
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///hospital.db
REDIS_URL=redis://localhost:6379/0
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 5. Install and Start Redis

**On Ubuntu/Debian:**
```bash
sudo apt-get install redis-server
sudo service redis-server start
```

**On macOS:**
```bash
brew install redis
brew services start redis
```

**On Windows:**
Download from https://redis.io/download or use WSL

## 🚀 Running the Application

### 1. Start Flask Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### 2. Start Celery Worker (in a new terminal)

```bash
# Activate virtual environment first
celery -A celery_worker.celery worker --loglevel=info
```

### 3. Start Celery Beat (in another terminal)

```bash
# Activate virtual environment first
celery -A celery_worker.celery beat --loglevel=info
```

### 4. Open Frontend

Open `frontend/index.html` in your browser or serve it using:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## 👥 Default Credentials

### Admin
- **Username**: `admin`
- **Password**: `admin123`

### Sample Doctor
- **Username**: `dr.sharma`
- **Password**: `doctor123`

### Patient
Register a new account through the frontend

## 📁 Project Structure

```
hospital-management-system-v2/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # Database models
│   ├── tasks.py              # Celery background tasks
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── admin.py         # Admin routes
│   │   ├── doctor.py        # Doctor routes
│   │   ├── patient.py       # Patient routes
│   │   └── api.py           # API routes
│   └── utils/
│       ├── init_db.py       # Database initialization
│       ├── decorators.py    # Role-based decorators
│       └── cache.py         # Redis caching utilities
├── frontend/
│   ├── index.html           # Main HTML file
│   └── app.js               # Vue.js application
├── config.py                # Configuration
├── run.py                   # Flask application runner
├── celery_worker.py         # Celery worker
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Patient registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

### Admin
- `GET /admin/dashboard` - Dashboard statistics
- `GET /admin/doctors` - List all doctors
- `POST /admin/doctors` - Add new doctor
- `PUT /admin/doctors/<id>` - Update doctor
- `DELETE /admin/doctors/<id>` - Deactivate doctor
- `GET /admin/patients` - List all patients
- `GET /admin/appointments` - List all appointments
- `GET /admin/search/doctors?q=query` - Search doctors
- `GET /admin/search/patients?q=query` - Search patients

### Doctor
- `GET /doctor/dashboard` - Dashboard statistics
- `GET /doctor/appointments` - List appointments
- `POST /doctor/appointments/<id>/complete` - Complete appointment
- `POST /doctor/appointments/<id>/cancel` - Cancel appointment
- `GET /doctor/patients/<id>/history` - Patient history
- `GET /doctor/availability` - Get availability
- `POST /doctor/availability` - Add availability slot

### Patient
- `GET /patient/dashboard` - Dashboard statistics
- `GET /patient/profile` - Get profile
- `PUT /patient/profile` - Update profile
- `GET /patient/specializations` - List specializations
- `GET /patient/doctors` - List doctors
- `GET /patient/doctors/<id>/availability` - Doctor availability
- `POST /patient/appointments` - Book appointment
- `GET /patient/appointments` - List appointments
- `POST /patient/appointments/<id>/cancel` - Cancel appointment
- `GET /patient/treatment-history` - Treatment history

### API
- `POST /api/export/treatments` - Export treatments as CSV
- `GET /api/export/status/<task_id>` - Check export status
- `GET /api/health` - Health check

## 🔄 Background Jobs

### Daily Reminders
- **Schedule**: Every day at 8:00 AM
- **Function**: Sends email reminders to patients with appointments scheduled for that day

### Monthly Reports
- **Schedule**: 1st of every month at 9:00 AM
- **Function**: Generates HTML reports of doctor activities and sends via email

### CSV Export
- **Trigger**: User-initiated
- **Function**: Exports patient treatment history as CSV and emails it

## 🗄️ Database Schema

### Users
- id, username, email, password_hash, role, is_active, created_at

### Patients
- id, user_id, full_name, date_of_birth, gender, contact_number, address, medical_history

### Doctors
- id, user_id, full_name, specialization_id, qualification, experience_years, consultation_fee, is_available

### Specializations
- id, name, description, created_at

### Appointments
- id, patient_id, doctor_id, appointment_date, appointment_time, status, reason, created_at, updated_at

### Treatments
- id, appointment_id, diagnosis, prescription, notes, next_visit_date, created_at

### DoctorAvailability
- id, doctor_id, date, start_time, end_time, is_booked

## 🎯 Key Features Implementation

### Role-Based Access Control
- Implemented using Flask-Login and custom decorators
- Each route is protected with role-specific decorators

### Appointment Conflict Prevention
- Checks for existing bookings before creating new appointments
- Validates doctor availability slots

### Caching with Redis
- Doctor listings cached for 10 minutes
- Specialization data cached for 1 hour
- Dashboard statistics cached for 5 minutes

### Async Task Processing
- CSV export runs asynchronously
- Email notifications sent via background workers
- Task status tracking available

## 🧪 Testing

### Test Admin Functions
1. Login as admin
2. Add a new doctor
3. View all appointments
4. Search for doctors/patients

### Test Doctor Functions
1. Login as doctor
2. View appointments
3. Complete an appointment with diagnosis
4. Add availability slots

### Test Patient Functions
1. Register new patient
2. Browse specializations
3. Book an appointment
4. View treatment history
5. Export CSV

## 🐛 Troubleshooting

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping
# Should return PONG
```

### Database Not Created
```bash
# Delete existing database and restart
rm hospital.db
python run.py
```

### Email Not Sending
- Check SMTP credentials in `.env`
- For Gmail, use App Password instead of regular password
- Enable "Less secure app access" or use OAuth2

### Celery Tasks Not Running
```bash
# Check Celery worker is running
celery -A celery_worker.celery inspect active
```

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

Created for IIT Madras BS Degree Project

## 🤝 Contributing

This is an academic project. For improvements or bug fixes, please create an issue or pull request.

## 📧 Support

For issues or questions, please open an issue on GitHub.
