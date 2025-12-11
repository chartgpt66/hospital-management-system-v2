# API Documentation

Base URL: `http://localhost:5000`

## Authentication

All authenticated endpoints require session cookies. Use `withCredentials: true` in requests.

### Register Patient
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "contact_number": "1234567890",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "address": "123 Main St"
}

Response: 201 Created
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "patient"
  }
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@hospital.com",
    "role": "admin"
  }
}
```

### Logout
```http
POST /auth/logout

Response: 200 OK
{
  "message": "Logout successful"
}
```

### Get Current User
```http
GET /auth/me

Response: 200 OK
{
  "id": 1,
  "username": "admin",
  "email": "admin@hospital.com",
  "role": "admin",
  "is_active": true
}
```

## Admin Endpoints

### Get Dashboard Statistics
```http
GET /admin/dashboard

Response: 200 OK
{
  "total_doctors": 10,
  "total_patients": 50,
  "total_appointments": 100,
  "pending_appointments": 20,
  "completed_appointments": 70,
  "cancelled_appointments": 10,
  "total_specializations": 6
}
```

### List All Doctors
```http
GET /admin/doctors

Response: 200 OK
[
  {
    "id": 1,
    "user_id": 2,
    "full_name": "Dr. Rajesh Sharma",
    "specialization": "Cardiology",
    "qualification": "MBBS, MD (Cardiology)",
    "experience_years": 15,
    "consultation_fee": 1000,
    "is_available": true,
    "email": "sharma@hospital.com",
    "username": "dr.sharma"
  }
]
```

### Add New Doctor
```http
POST /admin/doctors
Content-Type: application/json

{
  "username": "dr.patel",
  "email": "patel@hospital.com",
  "password": "doctor123",
  "full_name": "Dr. Priya Patel",
  "specialization_id": 2,
  "qualification": "MBBS, DM (Neurology)",
  "experience_years": 12,
  "consultation_fee": 1200
}

Response: 201 Created
{
  "message": "Doctor added successfully",
  "doctor_id": 2
}
```

### Update Doctor
```http
PUT /admin/doctors/1
Content-Type: application/json

{
  "full_name": "Dr. Rajesh Kumar Sharma",
  "consultation_fee": 1500,
  "is_available": true
}

Response: 200 OK
{
  "message": "Doctor updated successfully"
}
```

### Deactivate Doctor
```http
DELETE /admin/doctors/1

Response: 200 OK
{
  "message": "Doctor deactivated successfully"
}
```

### List All Patients
```http
GET /admin/patients

Response: 200 OK
[
  {
    "id": 1,
    "user_id": 3,
    "full_name": "John Doe",
    "email": "john@example.com",
    "contact_number": "1234567890",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "is_active": true
  }
]
```

### List All Appointments
```http
GET /admin/appointments

Response: 200 OK
[
  {
    "id": 1,
    "patient_name": "John Doe",
    "doctor_name": "Dr. Rajesh Sharma",
    "specialization": "Cardiology",
    "appointment_date": "2024-01-15",
    "appointment_time": "10:00:00",
    "status": "booked",
    "reason": "Chest pain"
  }
]
```

### Search Doctors
```http
GET /admin/search/doctors?q=cardio

Response: 200 OK
[
  {
    "id": 1,
    "full_name": "Dr. Rajesh Sharma",
    "specialization": "Cardiology",
    "qualification": "MBBS, MD (Cardiology)",
    "experience_years": 15,
    "is_available": true
  }
]
```

### Search Patients
```http
GET /admin/search/patients?q=john

Response: 200 OK
[
  {
    "id": 1,
    "full_name": "John Doe",
    "contact_number": "1234567890",
    "email": "john@example.com",
    "is_active": true
  }
]
```

## Doctor Endpoints

### Get Doctor Dashboard
```http
GET /doctor/dashboard

Response: 200 OK
{
  "upcoming_appointments_today": 5,
  "upcoming_appointments_week": 15,
  "total_patients": 50,
  "completed_appointments": 200
}
```

### List Doctor's Appointments
```http
GET /doctor/appointments?status=booked&date=2024-01-15

Response: 200 OK
[
  {
    "id": 1,
    "patient_id": 1,
    "patient_name": "John Doe",
    "patient_contact": "1234567890",
    "appointment_date": "2024-01-15",
    "appointment_time": "10:00:00",
    "status": "booked",
    "reason": "Chest pain"
  }
]
```

### Complete Appointment
```http
POST /doctor/appointments/1/complete
Content-Type: application/json

{
  "diagnosis": "Mild hypertension",
  "prescription": "Amlodipine 5mg once daily",
  "notes": "Follow up in 2 weeks",
  "next_visit_date": "2024-01-29"
}

Response: 200 OK
{
  "message": "Appointment completed successfully"
}
```

### Cancel Appointment
```http
POST /doctor/appointments/1/cancel

Response: 200 OK
{
  "message": "Appointment cancelled successfully"
}
```

### Get Patient History
```http
GET /doctor/patients/1/history

Response: 200 OK
[
  {
    "appointment_id": 1,
    "appointment_date": "2024-01-01",
    "diagnosis": "Common cold",
    "prescription": "Paracetamol 500mg",
    "notes": "Rest for 3 days",
    "next_visit_date": null
  }
]
```

### Get Doctor Availability
```http
GET /doctor/availability

Response: 200 OK
[
  {
    "id": 1,
    "date": "2024-01-15",
    "start_time": "09:00:00",
    "end_time": "12:00:00",
    "is_booked": false
  }
]
```

### Add Availability Slot
```http
POST /doctor/availability
Content-Type: application/json

{
  "date": "2024-01-20",
  "start_time": "14:00",
  "end_time": "17:00"
}

Response: 201 Created
{
  "message": "Availability added successfully"
}
```

## Patient Endpoints

### Get Patient Dashboard
```http
GET /patient/dashboard

Response: 200 OK
{
  "upcoming_appointments": 2,
  "total_appointments": 10,
  "completed_appointments": 8
}
```

### Get Patient Profile
```http
GET /patient/profile

Response: 200 OK
{
  "id": 1,
  "full_name": "John Doe",
  "email": "john@example.com",
  "date_of_birth": "1990-01-01",
  "gender": "Male",
  "contact_number": "1234567890",
  "address": "123 Main St",
  "medical_history": "No known allergies"
}
```

### Update Patient Profile
```http
PUT /patient/profile
Content-Type: application/json

{
  "full_name": "John Michael Doe",
  "contact_number": "9876543210",
  "address": "456 Oak Avenue"
}

Response: 200 OK
{
  "message": "Profile updated successfully"
}
```

### List Specializations
```http
GET /patient/specializations

Response: 200 OK
[
  {
    "id": 1,
    "name": "Cardiology",
    "description": "Heart and cardiovascular system",
    "doctors_count": 3
  }
]
```

### List Doctors by Specialization
```http
GET /patient/doctors?specialization_id=1

Response: 200 OK
[
  {
    "id": 1,
    "full_name": "Dr. Rajesh Sharma",
    "specialization": "Cardiology",
    "qualification": "MBBS, MD (Cardiology)",
    "experience_years": 15,
    "consultation_fee": 1000
  }
]
```

### Get Doctor Availability
```http
GET /patient/doctors/1/availability

Response: 200 OK
[
  {
    "id": 1,
    "date": "2024-01-15",
    "start_time": "09:00:00",
    "end_time": "12:00:00"
  }
]
```

### Book Appointment
```http
POST /patient/appointments
Content-Type: application/json

{
  "doctor_id": 1,
  "appointment_date": "2024-01-15",
  "appointment_time": "10:00",
  "reason": "Regular checkup"
}

Response: 201 Created
{
  "message": "Appointment booked successfully",
  "appointment_id": 1
}
```

### List Patient Appointments
```http
GET /patient/appointments?status=booked

Response: 200 OK
[
  {
    "id": 1,
    "doctor_name": "Dr. Rajesh Sharma",
    "specialization": "Cardiology",
    "appointment_date": "2024-01-15",
    "appointment_time": "10:00:00",
    "status": "booked",
    "reason": "Regular checkup"
  }
]
```

### Cancel Appointment
```http
POST /patient/appointments/1/cancel

Response: 200 OK
{
  "message": "Appointment cancelled successfully"
}
```

### Get Treatment History
```http
GET /patient/treatment-history

Response: 200 OK
[
  {
    "appointment_id": 1,
    "doctor_name": "Dr. Rajesh Sharma",
    "specialization": "Cardiology",
    "appointment_date": "2024-01-01",
    "diagnosis": "Mild hypertension",
    "prescription": "Amlodipine 5mg",
    "notes": "Follow up in 2 weeks",
    "next_visit_date": "2024-01-15"
  }
]
```

## API Endpoints

### Export Treatment History
```http
POST /api/export/treatments

Response: 202 Accepted
{
  "message": "Export started. You will receive an email when ready.",
  "task_id": "abc123-def456-ghi789"
}
```

### Check Export Status
```http
GET /api/export/status/abc123-def456-ghi789

Response: 200 OK
{
  "state": "SUCCESS",
  "status": "Export completed",
  "result": {
    "status": "success",
    "message": "CSV exported and sent via email",
    "records": 10
  }
}
```

### Health Check
```http
GET /api/health

Response: 200 OK
{
  "status": "healthy",
  "message": "Hospital Management System API is running"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Field 'email' is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied. Admin role required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error message"
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `202 Accepted` - Request accepted for processing
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
