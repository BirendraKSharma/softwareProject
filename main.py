from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from databases import db, User, Doctor, Appointment, init_db
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    doctors = Doctor.query.all()
    return render_template('home.html', doctors=doctors)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/doctors')
def doctors():
    search = request.args.get('search', '')
    specialty = request.args.get('specialty', '')
    query = Doctor.query
    if search:
        query = query.filter(Doctor.name.contains(search) | Doctor.specialty.contains(search))
    if specialty:
        query = query.filter(Doctor.specialty == specialty)
    doctors = query.all()
    specialties = db.session.query(Doctor.specialty).distinct().all()
    return render_template('doctors.html', doctors=doctors, specialties=specialties)

@app.route('/doctor/<int:doctor_id>')
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('doctor_profile.html', doctor=doctor)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not all([name, email, password, confirm_password]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return redirect(url_for('register'))
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered! Please login.', 'warning')
            return redirect(url_for('login'))
        new_user = User(name=name, email=email, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.created_at.desc()).all()
    return render_template('dashboard.html', appointments=appointments)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        new_password = request.form.get('new_password')
        if new_password:
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long!', 'danger')
                return redirect(url_for('profile'))
            current_user.set_password(new_password)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason')
        if not all([appointment_date, appointment_time, reason]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('book_appointment', doctor_id=doctor_id))
        appointment = Appointment(
            user_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason
        )
        db.session.add(appointment)
        db.session.commit()
        flash(f'Appointment booked successfully with Dr. {doctor.name}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('book_appointment.html', doctor=doctor)

@app.route('/cancel-appointment/<int:appointment_id>')
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.user_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('dashboard'))
    if appointment.status == 'Completed':
        flash('Cannot cancel completed appointment!', 'warning')
        return redirect(url_for('dashboard'))
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully!', 'info')
    return redirect(url_for('dashboard'))

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.filter_by(is_admin=False).count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='Pending').count()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_doctors=total_doctors,
                         total_appointments=total_appointments,
                         pending_appointments=pending_appointments,
                         recent_appointments=recent_appointments)

@app.route('/admin/doctors')
@login_required
@admin_required
def admin_doctors():
    doctors = Doctor.query.all()
    return render_template('admin_doctors.html', doctors=doctors)

@app.route('/admin/doctor/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        specialty = request.form.get('specialty')
        email = request.form.get('email')
        phone = request.form.get('phone')
        qualification = request.form.get('qualification')
        experience = request.form.get('experience')
        available_days = request.form.get('available_days')
        available_time = request.form.get('available_time')
        existing_doctor = Doctor.query.filter_by(email=email).first()
        if existing_doctor:
            flash('Doctor with this email already exists!', 'warning')
            return redirect(url_for('add_doctor'))
        doctor = Doctor(
            name=name,
            specialty=specialty,
            email=email,
            phone=phone,
            qualification=qualification,
            experience=int(experience) if experience else 0,
            available_days=available_days,
            available_time=available_time
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f'Doctor {name} added successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    return render_template('add_doctor.html')

@app.route('/admin/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.name = request.form.get('name')
        doctor.specialty = request.form.get('specialty')
        doctor.email = request.form.get('email')
        doctor.phone = request.form.get('phone')
        doctor.qualification = request.form.get('qualification')
        doctor.experience = int(request.form.get('experience', 0))
        doctor.available_days = request.form.get('available_days')
        doctor.available_time = request.form.get('available_time')
        db.session.commit()
        flash(f'Doctor {doctor.name} updated successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/admin/doctor/delete/<int:doctor_id>')
@login_required
@admin_required
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if doctor.appointments:
        flash('Cannot delete doctor with existing appointments!', 'danger')
        return redirect(url_for('admin_doctors'))
    db.session.delete(doctor)
    db.session.commit()
    flash(f'Doctor {doctor.name} deleted successfully!', 'success')
    return redirect(url_for('admin_doctors'))

@app.route('/admin/appointments')
@login_required
@admin_required
def admin_appointments():
    status_filter = request.args.get('status', '')
    query = Appointment.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    appointments = query.order_by(Appointment.created_at.desc()).all()
    return render_template('admin_appointments.html', appointments=appointments)

@app.route('/admin/appointment/<int:appointment_id>/update', methods=['POST'])
@login_required
@admin_required
def update_appointment_status(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    new_status = request.form.get('status')
    notes = request.form.get('notes')
    if new_status:
        appointment.status = new_status
    if notes:
        appointment.notes = notes
    db.session.commit()
    flash('Appointment updated successfully!', 'success')
    return redirect(url_for('admin_appointments'))

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin_users.html', users=users)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
