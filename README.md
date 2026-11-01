# Attenda — Student Management System (SMS)

A full-stack, enterprise-grade Student Management System built with **Python**, **Django**, **HTML5/CSS3/JavaScript**, and **SQLite**. Inspired by modern SaaS education portals like Attenda, AttendX, and Dribbble.

---

## 🌟 Key Features & Modules

### 🔐 Authentication & Access Control
- **Dual-Mode Login**: Authenticate with either **Username** or **Institutional Email Address**.
- **Interactive Password Visibility**: Show/Hide password toggle button.
- **Self-Service Registration**: New administrators/staff can create accounts and gain immediate access to the dashboard.
- **Forgot Password Flow**: Clean password reset request interface.
- **Session Control**: "Remember Me" option with persistent session tokens.

### 📊 Module 1: Dashboard / Home
- **Personalized Administrator Welcome**: Dynamic greeting with admin name and role.
- **Live Institutional Metrics**:
  - Total Enrolled Students
  - Total Academic Departments
  - Total Courses / Degree Programs
  - Average Institutional CGPA
- **Interactive Charts (Chart.js)**:
  - Department-wise student distribution bar chart.
  - Academic performance tier doughnut chart (Distinction, First Class, Second Class, Remedial).
- **Recently Enrolled Students**: Quick overview of recent registrations with direct profile access.
- **Quick Action Bar**: One-click shortcuts to Add Student, View Students, Add Department, and Add Course.

### 📝 Module 2: Add Student
- Structured multi-section student enrollment form:
  - **Personal Information**: Full Name, Gender, Date of Birth.
  - **Academic Details**: Department (dynamic dropdown), Course (cascading dynamic AJAX dropdown), Year/Semester, and CGPA (0.00 – 10.00).
  - **Contact Information**: Institutional Email, Phone Number, Residential Address.
  - **Student Photo**: Profile photo upload with **real-time client-side image preview**.
- Server-side and client-side validation with instant feedback alerts.

### 📋 Module 3: View & Manage Students
- **Responsive Data Table**: Avatar/initials, full name, register number, department, course, year/semester, status pill, and color-coded CGPA badge.
- **Administrative Actions**: View Profile, Edit Details, Delete Record (with confirmation safeguard).
- **Pagination**: Smooth page navigation handling large volumes of student records.
- **CSV Data Export**: One-click export of student records to a downloadable CSV spreadsheet.

### 🔍 Module 4: Search & Student Profile
- **Multi-Criteria Search & Filter**:
  - Search by Name, Register / Roll Number, or Email.
  - Filter by Department, Course, and Gender.
  - Sort by Newest, Oldest, Name (A-Z / Z-A), and Highest / Lowest CGPA.
- **Comprehensive Student Profile**:
  - Institutional ID card layout with student photo and registration credentials.
  - Academic scorecard breakdown (program length, credits, performance tier).
  - Personal and contact details card.
  - Printable ID card / profile feature (`window.print()`).

### 🏛️ Module 5: Department & Course Management
- **Department Management**:
  - Add, view, edit, and delete departments.
  - Displays live enrolled student and course capacity per department.
  - **Relational Integrity Protection**: Guarded deletion preventing removal of departments that have actively enrolled students.
- **Course Management**:
  - Add, edit, and view degree programs and diplomas.
  - Assign courses to departments with credit allocation and duration in years.
  - Real-time student enrollment count per course.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Language** | Python 3.13 |
| **Backend Framework** | Django 5.1 |
| **Database** | SQLite3 via Django ORM |
| **Frontend UI** | HTML5, CSS3, JavaScript (ES6+) |
| **CSS Framework** | Bootstrap 5.3 + Bootstrap Icons |
| **Data Visualizations** | Chart.js 4.4 |
| **Fonts** | Google Fonts (*Inter* & *Outfit*) |

---

## 🚀 Getting Started & How to Run

### 1. Requirements
Ensure you have Python 3.10+ installed.

### 2. Run Database Migrations (already initialized)
```bash
python manage.py migrate
```

### 3. Seed Sample Data (Optional / Pre-populated)
To populate departments, courses, and sample students:
```bash
python manage.py seed_data
```

### 4. Start the Django Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 🔑 Default Credentials

A default administrator account has been seeded:

- **Username**: `admin`
- **Email**: `admin@institution.edu`
- **Password**: `admin123`

*(You can also use the **"Create an Account"** button on the login screen to register your own staff account.)*

---

## 📂 Project Structure

```
Student_management/
│
├── manage.py                          # Django CLI entrypoint
├── db.sqlite3                         # SQLite database
│
├── student_system/                    # Project Configuration
│   ├── settings.py                    # Django settings & static/media config
│   ├── urls.py                        # Root URL router
│   ├── wsgi.py                        # WSGI entrypoint
│   └── asgi.py
│
├── students_app/                      # Core Student Management App
│   ├── models.py                      # Department, Course, Student models
│   ├── forms.py                       # StudentForm, DepartmentForm, CourseForm, User Forms
│   ├── views.py                       # Controllers for all 6 modules & auth
│   ├── urls.py                        # App route definitions
│   ├── backends.py                    # Email-or-Username custom authentication backend
│   ├── tests.py                       # Comprehensive 11-step automated test suite
│   ├── admin.py                       # Django admin configuration
│   └── management/
│       └── commands/
│           └── seed_data.py           # Database seeder script
│
├── templates/                         # HTML Templates
│   ├── base.html                      # Layout shell with sidebar and topbar
│   └── students_app/
│       ├── auth/
│       │   ├── login.html             # Login with show/hide password
│       │   ├── register.html          # New staff account registration
│       │   └── forgot_password.html   # Password reset request
│       ├── dashboard.html             # Module 1: Dashboard with KPI cards & charts
│       ├── students/
│       │   ├── student_list.html      # Module 3 & 4: Student directory & filter
│       │   ├── student_form.html      # Module 2: Add/Edit student with preview
│       │   ├── student_detail.html    # Module 4: Student profile & ID card
│       │   └── student_confirm_delete.html # Confirmation safeguard
│       ├── departments/
│       │   ├── department_list.html   # Module 5: Department cards & counts
│       │   ├── department_form.html   # Add/Edit department
│       │   └── department_confirm_delete.html # Safe delete verification
│       └── courses/
│           ├── course_list.html       # Course catalog & dept assignments
│           ├── course_form.html       # Add/Edit course
│           └── course_confirm_delete.html
│
├── static/                            # Static Assets
│   ├── css/
│   │   └── style.css                  # Custom styling & modern aesthetics
│   └── js/
│       └── main.js                    # Dynamic cascading dropdowns & UI interactions
│
└── media/                             # Uploaded media (student profile photos)
    └── student_photos/
```
