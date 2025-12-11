# Testing Guide

## Manual Testing Scenarios

### Prerequisites
- Application running on http://localhost:5000 (Backend)
- Frontend running on http://localhost:8000
- Redis server running
- Celery worker and beat running

## Test Scenario 1: Admin Functionality

### 1.1 Admin Login
```
Steps:
1. Open http://localhost:8000
2. Click "Login"
3. Enter username: admin
4. Enter password: admin123
5. Click "Login"

Expected Result:
✓ Redirected to admin dashboard
✓ Welcome message shows "Welcome, admin (admin)"
✓ Dashboard shows statistics
```

### 1.2 View Dashboard Statistics
```
Steps:
1. After login, view dashboard

Expected Result:
✓ Total Doctors count displayed
✓ Total Patients count displayed
✓ Total Appointments count displayed
✓ Pending/Completed/Cancelled counts shown
```

### 1.3 Manage Doctors
```
Steps:
1. Click "Manage Doctors" in sidebar
2. View list of doctors
3. Click "Add New Doctor"
4. Fill form:
   - Username: dr.test
   - Email: test@hospital.com
   - Password: doctor123
   - Full Name: Dr. Test Doctor
   - Specialization: Select from dropdown
   - Qualification: MBBS, MD
   - Experience: 5
   - Fee: 800
5. Submit form

Expected Result:
✓ Doctor added successfully
✓ New doctor appears in list
✓ Success message displayed
```

### 1.4 Search Doctors
```
Steps:
1. Go to "Manage Doctors"
2. Use search functionality
3. Search for "cardio"

Expected Result:
✓ Only cardiologists shown
✓ Search results accurate
```

### 1.5 Deactivate Doctor
```
Steps:
1. Go to "Manage Doctors"
2. Click "Deactivate" on a doctor
3. Confirm action

Expected Result:
✓ Doctor status changed to "Unavailable"
✓ Doctor cannot login
✓ Success message shown
```

### 1.6 View All Appointments
```
Steps:
1. Click "All Appointments" in sidebar
2. View appointment list

Expected Result:
✓ All appointments displayed
✓ Patient names shown
✓ Doctor names shown
✓ Status badges colored correctly
```

### 1.7 Search Patients
```
Steps:
1. Use patient search
2. Search by name or contact

Expected Result:
✓ Matching patients displayed
✓ Contact information shown
✓ Active status visible
```

## Test Scenario 2: Doctor Functionality

### 2.1 Doctor Login
```
Steps:
1. Logout if logged in
2. Click "Login"
3. Enter username: dr.sharma
4. Enter password: doctor123
5. Click "Login"

Expected Result:
✓ Redirected to doctor dashboard
✓ Welcome message shows doctor name
✓ Dashboard shows doctor statistics
```

### 2.2 View Dashboard
```
Steps:
1. After login, view dashboard

Expected Result:
✓ Upcoming appointments today count
✓ Upcoming appointments week count
✓ Total patients count
✓ Completed appointments count
```

### 2.3 View Appointments
```
Steps:
1. Click "My Appointments" in sidebar
2. View appointment list

Expected Result:
✓ Only doctor's appointments shown
✓ Patient names visible
✓ Contact numbers shown
✓ Status badges displayed
```

### 2.4 Complete Appointment
```
Steps:
1. Go to "My Appointments"
2. Find a "booked" appointment
3. Click "Complete"
4. Enter diagnosis: "Common cold"
5. Enter prescription: "Paracetamol 500mg"
6. Enter notes: "Rest for 3 days"
7. Submit

Expected Result:
✓ Appointment status changed to "completed"
✓ Treatment record created
✓ Success message displayed
```

### 2.5 View Patient History
```
Steps:
1. Complete an appointment first
2. View patient's previous appointments
3. Check treatment history

Expected Result:
✓ All previous appointments shown
✓ Diagnoses visible
✓ Prescriptions displayed
✓ Notes accessible
```

### 2.6 Manage Availability
```
Steps:
1. Click "Manage Availability"
2. Click "Add Availability"
3. Select date (tomorrow)
4. Set start time: 14:00
5. Set end time: 17:00
6. Submit

Expected Result:
✓ Availability slot added
✓ Slot appears in list
✓ Patients can see this slot
```

### 2.7 Cancel Appointment
```
Steps:
1. Go to "My Appointments"
2. Find a "booked" appointment
3. Click "Cancel"
4. Confirm

Expected Result:
✓ Appointment status changed to "cancelled"
✓ Availability slot freed
✓ Success message shown
```

## Test Scenario 3: Patient Functionality

### 3.1 Patient Registration
```
Steps:
1. Logout if logged in
2. Click "Register as Patient"
3. Fill form:
   - Username: patient_test
   - Email: patient@test.com
   - Password: patient123
   - Full Name: Test Patient
   - Contact: 9876543210
4. Submit

Expected Result:
✓ Registration successful
✓ Redirected to login
✓ Success message displayed
```

### 3.2 Patient Login
```
Steps:
1. Click "Login"
2. Enter username: patient_test
3. Enter password: patient123
4. Click "Login"

Expected Result:
✓ Redirected to patient dashboard
✓ Welcome message shows patient name
✓ Dashboard shows patient statistics
```

### 3.3 View Dashboard
```
Steps:
1. After login, view dashboard

Expected Result:
✓ Upcoming appointments count
✓ Total appointments count
✓ Completed appointments count
```

### 3.4 Browse Specializations
```
Steps:
1. Click "Find Doctors" in sidebar
2. View specialization cards

Expected Result:
✓ All specializations displayed
✓ Doctor counts shown
✓ Descriptions visible
✓ Cards clickable
```

### 3.5 Find Doctors
```
Steps:
1. Go to "Find Doctors"
2. Click on "Cardiology" card
3. View doctors list

Expected Result:
✓ Only cardiologists shown
✓ Qualifications displayed
✓ Experience shown
✓ Consultation fees visible
```

### 3.6 Check Doctor Availability
```
Steps:
1. Select a doctor
2. View availability for next 7 days

Expected Result:
✓ Available slots shown
✓ Dates displayed
✓ Time slots visible
✓ Only future dates shown
```

### 3.7 Book Appointment
```
Steps:
1. Select a doctor
2. Choose available date
3. Choose available time
4. Enter reason: "Regular checkup"
5. Submit booking

Expected Result:
✓ Appointment booked successfully
✓ Confirmation message shown
✓ Appointment appears in "My Appointments"
✓ Slot marked as booked
```

### 3.8 View Appointments
```
Steps:
1. Click "My Appointments"
2. View appointment list

Expected Result:
✓ All patient's appointments shown
✓ Doctor names visible
✓ Specializations shown
✓ Status badges displayed
```

### 3.9 Cancel Appointment
```
Steps:
1. Go to "My Appointments"
2. Find a "booked" appointment
3. Click "Cancel"
4. Confirm

Expected Result:
✓ Appointment cancelled
✓ Status changed to "cancelled"
✓ Slot becomes available again
```

### 3.10 View Treatment History
```
Steps:
1. Click "Treatment History"
2. View completed appointments

Expected Result:
✓ Only completed appointments shown
✓ Diagnoses visible
✓ Prescriptions displayed
✓ Doctor notes shown
✓ Next visit dates (if any)
```

### 3.11 Export Treatment History
```
Steps:
1. Go to "Treatment History"
2. Click "Export as CSV"
3. Wait for confirmation

Expected Result:
✓ Export task queued
✓ Confirmation message shown
✓ Email received with CSV attachment
✓ CSV contains all treatment data
```

### 3.12 Update Profile
```
Steps:
1. Click "My Profile"
2. Update contact number
3. Update address
4. Submit changes

Expected Result:
✓ Profile updated successfully
✓ Changes reflected immediately
✓ Success message displayed
```

## Test Scenario 4: Background Jobs

### 4.1 Daily Reminders
```
Setup:
1. Create appointment for today
2. Wait for 8 AM or manually trigger

Manual Trigger:
python -c "from app.tasks import send_daily_reminders; send_daily_reminders()"

Expected Result:
✓ Email sent to patient
✓ Email contains appointment details
✓ Doctor name included
✓ Time and date shown
```

### 4.2 Monthly Reports
```
Setup:
1. Have completed appointments in previous month
2. Wait for 1st of month or manually trigger

Manual Trigger:
python -c "from app.tasks import send_monthly_reports; send_monthly_reports()"

Expected Result:
✓ Email sent to doctors
✓ HTML report generated
✓ Statistics included
✓ Appointment details listed
```

### 4.3 CSV Export
```
Steps:
1. Login as patient
2. Go to "Treatment History"
3. Click "Export as CSV"
4. Check email

Expected Result:
✓ Task queued immediately
✓ Email received within 1 minute
✓ CSV file attached
✓ All treatment data included
```

## Test Scenario 5: Edge Cases

### 5.1 Double Booking Prevention
```
Steps:
1. Login as patient 1
2. Book appointment with Dr. Sharma at 10:00 AM
3. Logout
4. Login as patient 2
5. Try to book same slot

Expected Result:
✓ Error message: "This time slot is already booked"
✓ Booking prevented
✓ Slot not double-booked
```

### 5.2 Invalid Login
```
Steps:
1. Try to login with wrong password
2. Try to login with non-existent user

Expected Result:
✓ Error message: "Invalid username or password"
✓ Login prevented
✓ No sensitive information leaked
```

### 5.3 Unauthorized Access
```
Steps:
1. Login as patient
2. Try to access /admin/dashboard directly

Expected Result:
✓ Access denied
✓ Error: "Admin role required"
✓ Redirected or error shown
```

### 5.4 Deactivated User Login
```
Steps:
1. Admin deactivates a user
2. User tries to login

Expected Result:
✓ Error: "Account is deactivated"
✓ Login prevented
✓ Appropriate message shown
```

### 5.5 Past Date Booking
```
Steps:
1. Try to book appointment for past date

Expected Result:
✓ Booking prevented
✓ Error message shown
✓ Only future dates allowed
```

## Test Scenario 6: Performance & Caching

### 6.1 Cache Hit Test
```
Steps:
1. Load doctors list (first time)
2. Note response time
3. Load doctors list again (second time)
4. Note response time

Expected Result:
✓ Second load faster
✓ Data served from cache
✓ Cache TTL respected
```

### 6.2 Cache Invalidation
```
Steps:
1. Load doctors list (cached)
2. Admin adds new doctor
3. Load doctors list again

Expected Result:
✓ New doctor appears immediately
✓ Cache invalidated on update
✓ Fresh data served
```

## Test Scenario 7: API Testing

### 7.1 Health Check
```
curl http://localhost:5000/api/health

Expected Result:
{
  "status": "healthy",
  "message": "Hospital Management System API is running"
}
```

### 7.2 Login API
```
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

Expected Result:
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### 7.3 Get Dashboard Stats
```
curl http://localhost:5000/admin/dashboard \
  -H "Cookie: session=<session_cookie>"

Expected Result:
{
  "total_doctors": 3,
  "total_patients": 5,
  "total_appointments": 10,
  ...
}
```

## Automated Testing (Optional)

### Unit Tests Template
```python
# tests/test_models.py
def test_user_creation():
    user = User(username='test', email='test@test.com')
    assert user.username == 'test'

def test_appointment_booking():
    # Test appointment creation
    pass

def test_double_booking_prevention():
    # Test conflict detection
    pass
```

### Integration Tests Template
```python
# tests/test_api.py
def test_login_endpoint():
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200

def test_unauthorized_access():
    response = client.get('/admin/dashboard')
    assert response.status_code == 401
```

## Testing Checklist

### Functional Testing
- [ ] All user roles can login
- [ ] Admin can manage doctors
- [ ] Admin can manage patients
- [ ] Doctor can view appointments
- [ ] Doctor can complete appointments
- [ ] Patient can register
- [ ] Patient can book appointments
- [ ] Patient can view history
- [ ] Background jobs execute

### Security Testing
- [ ] Passwords are hashed
- [ ] Unauthorized access prevented
- [ ] Role-based access works
- [ ] SQL injection prevented
- [ ] XSS prevented

### Performance Testing
- [ ] Caching works correctly
- [ ] API response times acceptable
- [ ] Database queries optimized
- [ ] No N+1 query problems

### Usability Testing
- [ ] UI is intuitive
- [ ] Error messages clear
- [ ] Success messages shown
- [ ] Navigation easy
- [ ] Forms validated

## Bug Reporting Template

```
Title: [Brief description]

Steps to Reproduce:
1. 
2. 
3. 

Expected Result:


Actual Result:


Environment:
- Browser:
- OS:
- Python version:

Screenshots:
[Attach if applicable]
```

## Performance Benchmarks

### Expected Response Times
- Login: < 200ms
- Dashboard load: < 300ms
- Appointment booking: < 500ms
- CSV export trigger: < 100ms
- Search queries: < 200ms

### Database Queries
- Should use indexes
- No N+1 queries
- Proper joins used
- Pagination implemented

## Conclusion

Follow these test scenarios systematically to ensure all features work correctly. Report any issues found during testing with detailed steps to reproduce.
