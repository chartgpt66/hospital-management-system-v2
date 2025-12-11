# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Vue.js 3 Application (index.html + app.js)           │ │
│  │  - User Interface Components                           │ │
│  │  - Bootstrap 5 Styling                                 │ │
│  │  - Axios for API calls                                 │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer (Flask)                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Routes                                            │ │
│  │  ├── /auth/*      - Authentication                     │ │
│  │  ├── /admin/*     - Admin operations                   │ │
│  │  ├── /doctor/*    - Doctor operations                  │ │
│  │  ├── /patient/*   - Patient operations                 │ │
│  │  └── /api/*       - Utility APIs                       │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Business Logic                                        │ │
│  │  - Role-based access control                          │ │
│  │  - Data validation                                     │ │
│  │  - Error handling                                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
            ↓                           ↓
┌──────────────────────┐    ┌──────────────────────────────┐
│   Database Layer     │    │    Caching Layer (Redis)     │
│   ┌──────────────┐   │    │   ┌──────────────────────┐   │
│   │   SQLite     │   │    │   │  Doctor listings     │   │
│   │              │   │    │   │  Specializations     │   │
│   │  - Users     │   │    │   │  Dashboard stats     │   │
│   │  - Patients  │   │    │   │  (TTL: 5-60 min)    │   │
│   │  - Doctors   │   │    │   └──────────────────────┘   │
│   │  - Appts     │   │    └──────────────────────────────┘
│   │  - Treatments│   │
│   └──────────────┘   │
└──────────────────────┘
            ↓
┌─────────────────────────────────────────────────────────────┐
│              Background Jobs Layer (Celery)                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Celery Worker                                         │ │
│  │  ├── Daily Reminders (Scheduled: 8 AM)                │ │
│  │  ├── Monthly Reports (Scheduled: 1st, 9 AM)           │ │
│  │  └── CSV Export (On-demand)                           │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Celery Beat (Scheduler)                              │ │
│  │  - Manages scheduled tasks                            │ │
│  │  - Triggers jobs at specified times                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Email Service (SMTP)                       │
│  - Appointment reminders                                     │
│  - Monthly reports                                           │
│  - CSV export notifications                                  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### 1. User Authentication Flow

```
User → Frontend → POST /auth/login → Flask
                                      ↓
                                   Validate credentials
                                      ↓
                                   Create session
                                      ↓
                                   Return user data
                                      ↓
Frontend ← JSON Response ← Flask
```

### 2. Appointment Booking Flow

```
Patient → Select Doctor → Check Availability
                              ↓
                         POST /patient/appointments
                              ↓
                         Validate slot
                              ↓
                    Check for conflicts (DB)
                              ↓
                         Create appointment
                              ↓
                    Update availability slot
                              ↓
                    Invalidate cache (Redis)
                              ↓
                         Return success
```

### 3. Daily Reminder Job Flow

```
Celery Beat (8 AM) → Trigger task
                         ↓
                    Celery Worker
                         ↓
                Query appointments for today (DB)
                         ↓
                For each appointment:
                    ↓
                Get patient email
                    ↓
                Generate reminder email
                    ↓
                Send via SMTP
                    ↓
                Log result
```

### 4. CSV Export Flow

```
Patient → Click Export → POST /api/export/treatments
                              ↓
                         Queue Celery task
                              ↓
                         Return task_id
                              ↓
Patient ← Task queued notification

[Async Process]
Celery Worker → Fetch treatment data (DB)
                    ↓
                Generate CSV
                    ↓
                Create email with attachment
                    ↓
                Send via SMTP
                    ↓
                Update task status
```

## Database Schema Relationships

```
┌─────────────┐
│    Users    │
│  (Base)     │
│ - id        │
│ - username  │
│ - email     │
│ - password  │
│ - role      │
└──────┬──────┘
       │
       ├─────────────────────────────┐
       │                             │
       ↓                             ↓
┌─────────────┐              ┌─────────────┐
│  Patients   │              │   Doctors   │
│             │              │             │
│ - user_id   │              │ - user_id   │
│ - full_name │              │ - full_name │
│ - dob       │              │ - spec_id   │
│ - contact   │              │ - qual      │
└──────┬──────┘              └──────┬──────┘
       │                            │
       │                            │
       │      ┌──────────────┐      │
       └─────→│ Appointments │←─────┘
              │              │
              │ - patient_id │
              │ - doctor_id  │
              │ - date       │
              │ - time       │
              │ - status     │
              └──────┬───────┘
                     │
                     ↓
              ┌─────────────┐
              │ Treatments  │
              │             │
              │ - appt_id   │
              │ - diagnosis │
              │ - prescript │
              │ - notes     │
              └─────────────┘

┌──────────────────┐
│ Specializations  │
│                  │
│ - id             │
│ - name           │
│ - description    │
└────────┬─────────┘
         │
         │ (One-to-Many)
         ↓
    ┌─────────┐
    │ Doctors │
    └─────────┘

┌──────────────────────┐
│ DoctorAvailability   │
│                      │
│ - doctor_id          │
│ - date               │
│ - start_time         │
│ - end_time           │
│ - is_booked          │
└──────────────────────┘
```

## Component Interaction

### Admin Dashboard

```
Admin Login
    ↓
Dashboard View
    ├── GET /admin/dashboard (Stats)
    │   └── Cache: 5 min
    ├── GET /admin/doctors (List)
    │   └── Cache: 10 min
    ├── GET /admin/patients (List)
    └── GET /admin/appointments (List)
```

### Doctor Workflow

```
Doctor Login
    ↓
Dashboard View
    ├── GET /doctor/dashboard (Stats)
    ├── GET /doctor/appointments (Today)
    └── GET /doctor/availability (Week)
        ↓
View Appointment
    ↓
Complete Appointment
    ├── POST /doctor/appointments/{id}/complete
    ├── Add diagnosis
    ├── Add prescription
    └── Update status → 'completed'
```

### Patient Journey

```
Patient Registration
    ↓
POST /auth/register
    ↓
Login
    ↓
Browse Specializations
    ├── GET /patient/specializations
    │   └── Cache: 1 hour
    └── Select specialization
        ↓
View Doctors
    ├── GET /patient/doctors?spec_id=X
    │   └── Cache: 10 min
    └── Select doctor
        ↓
Check Availability
    ├── GET /patient/doctors/{id}/availability
    └── Select time slot
        ↓
Book Appointment
    └── POST /patient/appointments
        ├── Validate slot
        ├── Create appointment
        └── Update availability
```

## Caching Strategy

```
┌──────────────────────────────────────────────────┐
│              Redis Cache Keys                     │
├──────────────────────────────────────────────────┤
│ doctors:all              → 10 min TTL            │
│ doctors:spec:{id}        → 10 min TTL            │
│ specializations:all      → 1 hour TTL            │
│ dashboard:admin          → 5 min TTL             │
│ dashboard:doctor:{id}    → 5 min TTL             │
│ dashboard:patient:{id}   → 5 min TTL             │
└──────────────────────────────────────────────────┘

Cache Invalidation Triggers:
- Doctor added/updated/deleted → Clear doctors:*
- Appointment created/updated → Clear dashboard:*
- Specialization added → Clear specializations:*
```

## Security Layers

```
┌─────────────────────────────────────────────────┐
│  1. Authentication Layer                        │
│     - Flask-Login session management            │
│     - Bcrypt password hashing                   │
│     - Secure cookie handling                    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  2. Authorization Layer                         │
│     - Role-based decorators                     │
│     - @admin_required                           │
│     - @doctor_required                          │
│     - @patient_required                         │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  3. Validation Layer                            │
│     - Input validation                          │
│     - Data sanitization                         │
│     - Type checking                             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  4. Database Layer                              │
│     - SQLAlchemy ORM (SQL injection prevention) │
│     - Parameterized queries                     │
│     - Transaction management                    │
└─────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│              Production Setup                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Nginx      │      │  Gunicorn    │        │
│  │  (Reverse    │─────→│  (WSGI)      │        │
│  │   Proxy)     │      │  Flask App   │        │
│  └──────────────┘      └──────────────┘        │
│                              │                   │
│                              ↓                   │
│  ┌──────────────┐      ┌──────────────┐        │
│  │   Redis      │←────→│  Celery      │        │
│  │  (Cache +    │      │  Worker +    │        │
│  │   Broker)    │      │  Beat        │        │
│  └──────────────┘      └──────────────┘        │
│                              │                   │
│                              ↓                   │
│                        ┌──────────────┐         │
│                        │  PostgreSQL  │         │
│                        │  (Database)  │         │
│                        └──────────────┘         │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Technology Stack Details

```
┌─────────────────────────────────────────────────┐
│  Frontend                                        │
│  ├── Vue.js 3.x (CDN)                           │
│  ├── Bootstrap 5.3                              │
│  ├── Axios (HTTP client)                        │
│  └── Vanilla JavaScript                         │
├─────────────────────────────────────────────────┤
│  Backend                                         │
│  ├── Flask 3.0                                  │
│  ├── Flask-SQLAlchemy 3.1                       │
│  ├── Flask-Login 0.6                            │
│  ├── Flask-Bcrypt 1.0                           │
│  ├── Flask-Mail 0.9                             │
│  └── Flask-CORS 4.0                             │
├─────────────────────────────────────────────────┤
│  Database                                        │
│  ├── SQLite (Development)                       │
│  └── PostgreSQL (Production ready)              │
├─────────────────────────────────────────────────┤
│  Caching & Queue                                 │
│  ├── Redis 5.0                                  │
│  └── Celery 5.3                                 │
├─────────────────────────────────────────────────┤
│  Email                                           │
│  └── SMTP (Gmail/SendGrid)                      │
└─────────────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
    ├── Flask Instance 1
    ├── Flask Instance 2
    └── Flask Instance 3
         ↓
    Shared Redis
         ↓
    Database (Primary + Replicas)
```

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement connection pooling
- Use CDN for static assets

### Future Enhancements
- Microservices architecture
- Message queue (RabbitMQ)
- Containerization (Docker)
- Orchestration (Kubernetes)
- API Gateway
- Service mesh
