# Quick Reference Card

## 🚀 One-Command Setup

```bash
# Clone and setup
git clone https://github.com/chartgpt66/hospital-management-system-v2.git
cd hospital-management-system-v2
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

## ▶️ Start Commands

```bash
# Terminal 1 - Flask API
python run.py

# Terminal 2 - Celery Worker
celery -A celery_worker.celery worker --loglevel=info

# Terminal 3 - Celery Beat
celery -A celery_worker.celery beat --loglevel=info

# Terminal 4 - Frontend
cd frontend && python -m http.server 8000
```

## 🔑 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Doctor | `dr.sharma` | `doctor123` |
| Patient | Register new account | - |

## 🌐 URLs

- **Frontend**: http://localhost:8000
- **API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 📊 Database Tables

```
users → patients → appointments → treatments
users → doctors → appointments
specializations → doctors
doctors → doctor_availability
```

## 🔧 Common Commands

### Database
```bash
# Reset database
rm hospital.db && python run.py

# View database
sqlite3 hospital.db
.tables
.schema users
SELECT * FROM users;
```

### Redis
```bash
# Check Redis
redis-cli ping

# View cache keys
redis-cli KEYS "*"

# Clear cache
redis-cli FLUSHALL
```

### Celery
```bash
# Check active tasks
celery -A celery_worker.celery inspect active

# Check scheduled tasks
celery -A celery_worker.celery inspect scheduled

# Purge all tasks
celery -A celery_worker.celery purge
```

## 📡 Key API Endpoints

### Authentication
```
POST /auth/register    - Register patient
POST /auth/login       - Login user
POST /auth/logout      - Logout user
GET  /auth/me          - Get current user
```

### Admin
```
GET  /admin/dashboard           - Dashboard stats
GET  /admin/doctors             - List doctors
POST /admin/doctors             - Add doctor
PUT  /admin/doctors/{id}        - Update doctor
DELETE /admin/doctors/{id}      - Deactivate doctor
GET  /admin/appointments        - All appointments
GET  /admin/search/doctors?q=   - Search doctors
GET  /admin/search/patients?q=  - Search patients
```

### Doctor
```
GET  /doctor/dashboard                      - Dashboard stats
GET  /doctor/appointments                   - List appointments
POST /doctor/appointments/{id}/complete     - Complete appointment
POST /doctor/appointments/{id}/cancel       - Cancel appointment
GET  /doctor/patients/{id}/history          - Patient history
GET  /doctor/availability                   - Get availability
POST /doctor/availability                   - Add availability
```

### Patient
```
GET  /patient/dashboard                     - Dashboard stats
GET  /patient/profile                       - Get profile
PUT  /patient/profile                       - Update profile
GET  /patient/specializations               - List specializations
GET  /patient/doctors                       - List doctors
GET  /patient/doctors/{id}/availability     - Doctor availability
POST /patient/appointments                  - Book appointment
GET  /patient/appointments                  - List appointments
POST /patient/appointments/{id}/cancel      - Cancel appointment
GET  /patient/treatment-history             - Treatment history
```

### Utility
```
POST /api/export/treatments         - Export CSV
GET  /api/export/status/{task_id}   - Check export status
GET  /api/health                    - Health check
```

## 🎯 Testing Workflow

### Admin Test
```
1. Login: admin/admin123
2. Add doctor
3. View appointments
4. Search doctors
```

### Doctor Test
```
1. Login: dr.sharma/doctor123
2. View appointments
3. Complete appointment
4. Add availability
```

### Patient Test
```
1. Register new account
2. Browse specializations
3. Book appointment
4. View history
5. Export CSV
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Redis error | `redis-server` or `brew services start redis` |
| Port in use | Change port in `run.py` |
| Database error | `rm hospital.db && python run.py` |
| Email not sending | Check `.env` Gmail App Password |
| Celery not working | Ensure Redis is running |

## 📦 Project Structure

```
hospital-management-system-v2/
├── app/
│   ├── routes/          # API endpoints
│   ├── models.py        # Database models
│   ├── tasks.py         # Celery jobs
│   └── utils/           # Helpers
├── frontend/
│   ├── index.html       # UI
│   └── app.js           # Vue logic
├── config.py            # Settings
├── run.py               # Flask runner
└── celery_worker.py     # Celery runner
```

## 🔐 Security Features

- ✅ Bcrypt password hashing
- ✅ Session-based auth
- ✅ Role-based access control
- ✅ SQL injection prevention
- ✅ Input validation

## 📈 Performance Features

- ✅ Redis caching (5-60 min TTL)
- ✅ Async task processing
- ✅ Optimized queries
- ✅ Cache invalidation

## 🎨 UI Features

- ✅ Responsive design
- ✅ Bootstrap 5 styling
- ✅ Vue.js reactivity
- ✅ Clean interface

## 📝 Background Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| Daily Reminders | 8 AM daily | Email appointment reminders |
| Monthly Reports | 1st, 9 AM | Email doctor activity reports |
| CSV Export | On-demand | Email treatment history CSV |

## 🔄 Cache Strategy

| Key | TTL | Invalidation |
|-----|-----|--------------|
| `doctors:*` | 10 min | On doctor update |
| `specializations:*` | 1 hour | On spec update |
| `dashboard:*` | 5 min | On data change |

## 📊 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## 🎓 Academic Compliance

✅ Flask API
✅ Vue.js UI
✅ Bootstrap styling
✅ SQLite database
✅ Redis caching
✅ Celery jobs
✅ Programmatic DB creation
✅ Pre-created admin
✅ Three user roles
✅ All features implemented

## 📚 Documentation Files

- `README.md` - Main documentation
- `SETUP_GUIDE.md` - Installation steps
- `API_DOCUMENTATION.md` - API reference
- `TESTING_GUIDE.md` - Test scenarios
- `ARCHITECTURE.md` - System design
- `FEATURES_CHECKLIST.md` - Feature tracking
- `PROJECT_SUMMARY.md` - Overview
- `QUICK_REFERENCE.md` - This file

## 🆘 Need Help?

1. Check `SETUP_GUIDE.md` for installation
2. Check `TESTING_GUIDE.md` for testing
3. Check `API_DOCUMENTATION.md` for endpoints
4. Check terminal logs for errors
5. Ensure all services running

## 💡 Pro Tips

- Use `redis-cli MONITOR` to watch cache activity
- Use `celery -A celery_worker.celery events` to monitor tasks
- Check `hospital.db` with DB Browser for SQLite
- Use browser DevTools Network tab for API debugging
- Keep all 4 terminals open for full functionality

## 🎯 Quick Demo Script

```bash
# 1. Start everything
python run.py &
celery -A celery_worker.celery worker -l info &
celery -A celery_worker.celery beat -l info &
cd frontend && python -m http.server 8000 &

# 2. Open browser
open http://localhost:8000

# 3. Test admin
# Login: admin/admin123
# Add doctor, view stats

# 4. Test doctor
# Login: dr.sharma/doctor123
# View appointments, add availability

# 5. Test patient
# Register new account
# Book appointment, view history
```

## 📞 Support

- GitHub: https://github.com/chartgpt66/hospital-management-system-v2
- Issues: Create GitHub issue
- Docs: Check documentation files

---

**Last Updated**: December 2024
**Version**: 2.0
**Status**: Production Ready ✅
