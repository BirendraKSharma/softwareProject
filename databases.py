from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for patients"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with appointments
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Doctor(db.Model):
    """Doctor model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    qualification = db.Column(db.String(200))
    experience = db.Column(db.Integer)  # years of experience
    available_days = db.Column(db.String(200))  # e.g., "Mon,Wed,Fri"
    available_time = db.Column(db.String(100))  # e.g., "9:00 AM - 5:00 PM"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with appointments
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
    def __repr__(self):
        return f'<Doctor {self.name}>'


class Appointment(db.Model):
    """Appointment model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.String(20), nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')  # Pending, Confirmed, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)  # Doctor's notes
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'


def init_db(app):
    """Initialize database with sample data"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@hms.com').first()
        if not admin:
            admin = User(
                name='Admin',
                email='admin@hms.com',
                phone='1234567890',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create sample doctors if not exists
        if Doctor.query.count() == 0:
            doctors = [
                Doctor(
                    name='Dr. Birendra Sharma',
                    specialty='Cardiologist',
                    email='birendrasha444@gmail.com',
                    phone='9841234567',
                    qualification='MD, DM (Cardiology)',
                    experience=15,
                    available_days='Mon,Wed,Fri',
                    available_time='9:00 AM - 5:00 PM'
                ),
                Doctor(
                    name='Dr. Bishal Regmi',
                    specialty='Gynecologist',
                    email='bishalregmi180@gmail.com',
                    phone='9841234568',
                    qualification='MD (Gynecology)',
                    experience=10,
                    available_days='Tue,Thu,Sat',
                    available_time='10:00 AM - 4:00 PM'
                ),
                Doctor(
                    name='Dr. Anuj Thapa',
                    specialty='Ophthalmologist',
                    email='anujth345@gmail.com',
                    phone='9841234569',
                    qualification='MS (Ophthalmology)',
                    experience=8,
                    available_days='Mon,Tue,Wed,Thu,Fri',
                    available_time='8:00 AM - 3:00 PM'
                ),
                Doctor(
                    name='Dr. Biswas Kafle',
                    specialty='Otolaryngologist',
                    email='biswaskafle@gmail.com',
                    phone='9841234570',
                    qualification='MS (ENT)',
                    experience=12,
                    available_days='Mon,Wed,Fri,Sat',
                    available_time='11:00 AM - 6:00 PM'
                )
            ]
            
            for doctor in doctors:
                db.session.add(doctor)
        
        db.session.commit()
        print("Database initialized successfully!")
