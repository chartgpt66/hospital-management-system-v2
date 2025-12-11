# Quick Setup Guide

## Step-by-Step Installation

### 1. System Requirements
- Python 3.8 or higher
- Redis Server
- Git

### 2. Install Python Dependencies

```bash
# Clone repository
git clone https://github.com/chartgpt66/hospital-management-system-v2.git
cd hospital-management-system-v2

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Install Redis

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Windows:**
- Download Redis from https://github.com/microsoftarchive/redis/releases
- Or use WSL (Windows Subsystem for Linux)

### 4. Configure Application

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# Minimum required: Set SECRET_KEY and email credentials
```

### 5. Run Application

**Terminal 1 - Flask Server:**
```bash
python run.py
```

**Terminal 2 - Celery Worker:**
```bash
celery -A celery_worker.celery worker --loglevel=info
```

**Terminal 3 - Celery Beat (for scheduled tasks):**
```bash
celery -A celery_worker.celery beat --loglevel=info
```

**Terminal 4 - Frontend Server:**
```bash
cd frontend
python -m http.server 8000
```

### 6. Access Application

- **Frontend**: http://localhost:8000
- **API**: http://localhost:5000
- **Admin Login**: username=`admin`, password=`admin123`
- **Doctor Login**: username=`dr.sharma`, password=`doctor123`

## Common Issues

### Issue: Redis Connection Failed
**Solution:**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start it:
sudo service redis-server start  # Linux
brew services start redis         # macOS
```

### Issue: Database Not Found
**Solution:**
```bash
# The database is created automatically on first run
# If issues persist, delete and recreate:
rm hospital.db
python run.py
```

### Issue: Email Not Sending
**Solution:**
1. For Gmail, use App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Generate password for "Mail"
   - Use this in `.env` file

2. Update `.env`:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Issue: Celery Tasks Not Running
**Solution:**
```bash
# Ensure Redis is running
redis-cli ping

# Check Celery worker status
celery -A celery_worker.celery inspect active

# Restart worker if needed
# Press Ctrl+C to stop, then restart
```

## Testing the Application

### 1. Test Admin Functions
```
1. Login with admin/admin123
2. Go to "Manage Doctors"
3. Add a new doctor
4. View all appointments
5. Search for doctors
```

### 2. Test Doctor Functions
```
1. Login with dr.sharma/doctor123
2. View dashboard statistics
3. Check appointments
4. Add availability slots
```

### 3. Test Patient Functions
```
1. Click "Register as Patient"
2. Fill registration form
3. Login with new credentials
4. Browse specializations
5. Book an appointment
6. View treatment history
```

## Development Tips

### View Database
```bash
# Install DB Browser for SQLite
# Open hospital.db file to view tables

# Or use Python:
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     from app.models import User
...     users = User.query.all()
...     print(users)
```

### Check Redis Cache
```bash
redis-cli
> KEYS *
> GET "key-name"
> FLUSHALL  # Clear all cache
```

### Monitor Celery Tasks
```bash
# View active tasks
celery -A celery_worker.celery inspect active

# View scheduled tasks
celery -A celery_worker.celery inspect scheduled

# View registered tasks
celery -A celery_worker.celery inspect registered
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker (Optional)
```dockerfile
# Create Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Environment Variables for Production
```env
SECRET_KEY=generate-strong-random-key
DATABASE_URL=postgresql://user:pass@host/db  # Use PostgreSQL
REDIS_URL=redis://redis-host:6379/0
DEBUG=False
```

## Need Help?

- Check README.md for detailed documentation
- Review API endpoints in README.md
- Check error logs in terminal
- Ensure all services (Flask, Redis, Celery) are running

## Quick Commands Reference

```bash
# Start everything
python run.py                                          # Terminal 1
celery -A celery_worker.celery worker -l info         # Terminal 2
celery -A celery_worker.celery beat -l info           # Terminal 3
cd frontend && python -m http.server 8000             # Terminal 4

# Check status
redis-cli ping                                         # Redis
celery -A celery_worker.celery inspect active         # Celery

# Reset database
rm hospital.db && python run.py

# Clear cache
redis-cli FLUSHALL
```
