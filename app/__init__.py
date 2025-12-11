from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
import redis
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
redis_client = None

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Initialize Redis
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import auth, admin, doctor, patient, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(doctor.bp)
    app.register_blueprint(patient.bp)
    app.register_blueprint(api.bp)
    
    # Create database tables and admin user
    with app.app_context():
        db.create_all()
        from app.utils.init_db import create_admin_user, create_sample_data
        create_admin_user()
        create_sample_data()
    
    return app
