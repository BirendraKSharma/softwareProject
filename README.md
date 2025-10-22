# ��� Hospital Management System (HMS)

A modern, responsive web application for managing hospital operations, built with Flask and Bootstrap 5.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)

## ��� Overview

This Hospital Management System is a web-based application built using Python and Flask. It provides a comprehensive platform for managing hospital operations including patient registration, appointment booking, doctor management, and administrative controls.

## ✨ Features

### For Patients
- ��� User Registration & Login - Secure account creation with password encryption
- ���‍⚕️ Browse Doctors - View all available doctors with their specialties
- ��� Book Appointments - Schedule appointments with preferred doctors
- ��� Appointment Dashboard - View and manage your appointments
- ❌ Cancel Appointments - Cancel upcoming appointments when needed
- ��� Profile Management - Update personal information

### For Administrators
- ��� Admin Panel - Comprehensive dashboard for hospital management
- ��� User Management - View and manage registered users
- ��� Doctor Management - Add, edit, and remove doctors
- ��� Appointment Management - View all appointments with filtering
- ��� Search & Filter - Advanced search for doctors and appointments
- ��� Statistics Dashboard - View key metrics

### UI/UX Features
- ��� Fully Responsive - Works on desktop, tablet, and mobile
- ��� Modern Design - Clean interface with gradients and animations
- ��� Color-Coded Status - Visual indicators for appointment status
- ⚡ Fast Performance - Optimized loading and navigation

## ��� Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. Navigate to project directory:
```bash
cd d:/programming/project/hms
```

2. Create virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python main.py
```

6. Open browser and go to: `http://localhost:5000`

### Default Admin Login
- Email: `admin@hms.com`
- Password: `admin123`

## ��� Project Structure

```
hms/
├── main.py              # Main Flask application
├── databases.py         # Database models
├── requirements.txt     # Dependencies
├── README.md           # Documentation
├── static/
│   ├── style.css       # Custom CSS
│   ├── hospital.jpg    # Images
│   └── system.png
└── templates/          # 18 HTML templates
    ├── base.html
    ├── home.html
    ├── dashboard.html
    ├── admin_dashboard.html
    └── ...
```

## ���️ Technologies

- Backend: Flask 3.0.0, Flask-SQLAlchemy, Flask-Login
- Database: SQLite
- Frontend: HTML5, CSS3, Bootstrap 5.3.0
- Security: Werkzeug password hashing
- Icons: SVG icons

## ��� Usage Guide

### For Patients
1. Register a new account
2. Login with your credentials
3. Browse available doctors
4. Book an appointment by selecting doctor and date/time
5. View appointments in dashboard
6. Cancel if needed

### For Administrators
1. Login with admin credentials
2. Access Admin Panel from navigation
3. Manage doctors, appointments, and users
4. Use search and filter options
5. View statistics

## ��� Troubleshooting

**Database Issues**: Delete the `instance` folder and restart to recreate database

**Port In Use**: Change port in main.py: `app.run(debug=True, port=5001)`

**Dependencies Error**: Update pip: `pip install --upgrade pip`

## ��� Customization

Change colors in `static/style.css`:
```css
:root {
    --primary-color: #4CAF50;
    --secondary-color: #2196F3;
}
```

## ��� License

MIT License - Open source and free to use

---

**Built with ❤️ using Flask and Bootstrap**
