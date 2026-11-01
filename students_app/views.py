import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator

from .models import Department, Course, Student
from .forms import StudentForm, DepartmentForm, CourseForm, UserLoginForm, UserRegisterForm


# ==============================================================================
# AUTHENTICATION VIEWS
# ==============================================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)  # Browser close session
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                
                messages.success(request, f"Welcome back, {user.first_name or user.username}! You have successfully logged in.")
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username/email or password. Please verify your credentials and try again.")
        else:
            messages.error(request, "Please fill in all required fields properly.")
            
    return render(request, 'students_app/auth/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            
            # Automatically log the new user in
            login(request, user, backend='students_app.backends.EmailOrUsernameModelBackend')
            messages.success(request, f"Account created successfully! Welcome to the Admin Portal, {user.first_name or user.username}.")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
                    
    return render(request, 'students_app/auth/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('login')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            messages.success(request, f"If an account exists for '{email}', a password reset link has been dispatched to your inbox.")
            return redirect('login')
        else:
            messages.error(request, "Please enter a valid email address.")
    return render(request, 'students_app/auth/forgot_password.html')


# ==============================================================================
# MODULE 1: DASHBOARD / HOME
# ==============================================================================

@login_required
def dashboard_view(request):
    # Key statistics
    total_students = Student.objects.count()
    total_departments = Department.objects.count()
    total_courses = Course.objects.count()
    
    # Average CGPA calculation
    cgpa_stat = Student.objects.aggregate(avg_cgpa=Avg('cgpa'))
    avg_cgpa = round(cgpa_stat['avg_cgpa'], 2) if cgpa_stat['avg_cgpa'] else 0.0

    # Recently added students (latest 6)
    recent_students = Student.objects.select_related('department', 'course').order_by('-created_at')[:6]

    # Department student distribution for charts
    dept_distribution = Department.objects.annotate(student_count=Count('students')).values('name', 'code', 'student_count')
    dept_names = [d['code'] or d['name'] for d in dept_distribution]
    dept_counts = [d['student_count'] for d in dept_distribution]

    # CGPA Performance breakdown
    distinction_count = Student.objects.filter(cgpa__gte=8.5).count()
    first_class_count = Student.objects.filter(cgpa__gte=7.0, cgpa__lt=8.5).count()
    second_class_count = Student.objects.filter(cgpa__gte=5.0, cgpa__lt=7.0).count()
    pass_count = Student.objects.filter(cgpa__lt=5.0).count()

    # Gender breakdown
    gender_counts = {
        'Male': Student.objects.filter(gender='Male').count(),
        'Female': Student.objects.filter(gender='Female').count(),
        'Other': Student.objects.filter(gender='Other').count(),
    }

    context = {
        'total_students': total_students,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'avg_cgpa': avg_cgpa,
        'recent_students': recent_students,
        'dept_names': dept_names,
        'dept_counts': dept_counts,
        'distinction_count': distinction_count,
        'first_class_count': first_class_count,
        'second_class_count': second_class_count,
        'pass_count': pass_count,
        'gender_counts': gender_counts,
    }
    return render(request, 'students_app/dashboard.html', context)


# ==============================================================================
# MODULE 2: ADD STUDENT
# ==============================================================================

@login_required
def student_create_view(request):
    departments = Department.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student '{student.name}' ({student.register_number}) has been enrolled successfully!")
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, "Please correct the errors in the form before saving.")
    else:
        form = StudentForm()

    return render(request, 'students_app/students/student_form.html', {
        'form': form,
        'title': 'Add New Student',
        'subtitle': 'Enroll a new student into the institution database',
        'is_edit': False,
        'departments': departments,
        'courses': courses,
    })


# ==============================================================================
# MODULE 3 & 4: VIEW & MANAGE STUDENTS & SEARCH / DETAILS
# ==============================================================================

@login_required
def student_list_view(request):
    query = request.GET.get('q', '').strip()
    dept_id = request.GET.get('department', '')
    course_id = request.GET.get('course', '')
    gender = request.GET.get('gender', '')
    year_semester = request.GET.get('year_semester', '')
    sort_by = request.GET.get('sort', '-created_at')

    students = Student.objects.select_related('department', 'course').all()

    # Search filter
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(register_number__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    # Department filter
    if dept_id:
        students = students.filter(department_id=dept_id)

    # Course filter
    if course_id:
        students = students.filter(course_id=course_id)

    # Gender filter
    if gender:
        students = students.filter(gender=gender)

    # Year/Semester filter
    if year_semester:
        students = students.filter(year_semester=year_semester)

    # Sorting
    valid_sorts = {
        'name_asc': 'name',
        'name_desc': '-name',
        'reg_asc': 'register_number',
        'reg_desc': '-register_number',
        'cgpa_desc': '-cgpa',
        'cgpa_asc': 'cgpa',
        'newest': '-created_at',
        'oldest': 'created_at',
    }
    students = students.order_by(valid_sorts.get(sort_by, '-created_at'))

    # Pagination
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    departments = Department.objects.all()
    courses = Course.objects.all()

    context = {
        'page_obj': page_obj,
        'students': page_obj,
        'departments': departments,
        'courses': courses,
        'query': query,
        'selected_dept': dept_id,
        'selected_course': course_id,
        'selected_gender': gender,
        'selected_year_sem': year_semester,
        'selected_sort': sort_by,
        'total_results': paginator.count,
    }
    return render(request, 'students_app/students/student_list.html', context)


@login_required
def student_detail_view(request, pk):
    student = get_object_or_404(Student.objects.select_related('department', 'course'), pk=pk)
    return render(request, 'students_app/students/student_detail.html', {'student': student})


@login_required
def student_edit_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    departments = Department.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            updated_student = form.save()
            messages.success(request, f"Student details for '{updated_student.name}' updated successfully!")
            return redirect('student_detail', pk=updated_student.pk)
        else:
            messages.error(request, "Failed to update. Please review errors below.")
    else:
        form = StudentForm(instance=student)

    return render(request, 'students_app/students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Edit Student: {student.name}',
        'subtitle': f'Update student profile details and academic status ({student.register_number})',
        'is_edit': True,
        'departments': departments,
        'courses': courses,
    })


@login_required
def student_delete_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        reg_no = student.register_number
        student.delete()
        messages.success(request, f"Student '{name}' ({reg_no}) was deleted successfully.")
        return redirect('student_list')
    
    return render(request, 'students_app/students/student_confirm_delete.html', {'student': student})


@login_required
def export_students_csv(request):
    """Export filtered or all student records as a downloadable CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_directory.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Register No', 'Full Name', 'Email', 'Phone', 'Gender', 
        'Date of Birth', 'Department', 'Course', 'Year/Semester', 
        'CGPA', 'Status', 'Date Enrolled'
    ])

    students = Student.objects.select_related('department', 'course').all()
    for s in students:
        writer.writerow([
            s.register_number,
            s.name,
            s.email,
            s.phone,
            s.gender,
            s.date_of_birth.strftime('%Y-%m-%d') if s.date_of_birth else '',
            s.department.name if s.department else '',
            s.course.name if s.course else '',
            s.year_semester,
            s.cgpa,
            s.status,
            s.created_at.strftime('%Y-%m-%d'),
        ])

    return response


# ==============================================================================
# MODULE 5: DEPARTMENT & COURSE MANAGEMENT
# ==============================================================================

@login_required
def department_list_view(request):
    departments = Department.objects.annotate(
        total_students=Count('students', distinct=True),
        total_courses=Count('courses', distinct=True)
    ).all()
    return render(request, 'students_app/departments/department_list.html', {'departments': departments})


@login_required
def department_create_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f"Department '{dept.name}' ({dept.code}) created successfully.")
            return redirect('department_list')
        else:
            messages.error(request, "Failed to create department. Please check errors.")
    else:
        form = DepartmentForm()
    return render(request, 'students_app/departments/department_form.html', {
        'form': form,
        'title': 'Add New Department',
        'is_edit': False
    })


@login_required
def department_edit_view(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f"Department '{dept.name}' updated successfully.")
            return redirect('department_list')
        else:
            messages.error(request, "Failed to update department.")
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'students_app/departments/department_form.html', {
        'form': form,
        'dept': dept,
        'title': f'Edit Department: {dept.code}',
        'is_edit': True
    })


@login_required
def department_delete_view(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    # Check if department is linked to students
    student_count = dept.students.count()
    course_count = dept.courses.count()

    if request.method == 'POST':
        if student_count > 0:
            messages.error(request, f"Cannot delete '{dept.name}' because {student_count} student(s) are actively enrolled in it. Reassign or remove students first.")
            return redirect('department_list')
        
        name = dept.name
        dept.delete()
        messages.success(request, f"Department '{name}' has been deleted successfully.")
        return redirect('department_list')

    return render(request, 'students_app/departments/department_confirm_delete.html', {
        'dept': dept,
        'student_count': student_count,
        'course_count': course_count
    })


# ---------------- COURSE VIEWS ----------------

@login_required
def course_list_view(request):
    courses = Course.objects.select_related('department').annotate(
        total_students=Count('students')
    ).all()
    return render(request, 'students_app/courses/course_list.html', {'courses': courses})


@login_required
def course_create_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course '{course.name}' [{course.code}] added successfully.")
            return redirect('course_list')
        else:
            messages.error(request, "Failed to add course. Please check the form errors.")
    else:
        form = CourseForm()
    return render(request, 'students_app/courses/course_form.html', {
        'form': form,
        'title': 'Add New Course',
        'is_edit': False
    })


@login_required
def course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.name}' updated successfully.")
            return redirect('course_list')
        else:
            messages.error(request, "Failed to update course.")
    else:
        form = CourseForm(instance=course)
    return render(request, 'students_app/courses/course_form.html', {
        'form': form,
        'course': course,
        'title': f'Edit Course: {course.code}',
        'is_edit': True
    })


@login_required
def course_delete_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    student_count = course.students.count()

    if request.method == 'POST':
        if student_count > 0:
            messages.error(request, f"Cannot delete course '{course.name}' because {student_count} student(s) are enrolled in it. Reassign or remove students first.")
            return redirect('course_list')
        
        name = course.name
        course.delete()
        messages.success(request, f"Course '{name}' has been deleted successfully.")
        return redirect('course_list')

    return render(request, 'students_app/courses/course_confirm_delete.html', {
        'course': course,
        'student_count': student_count
    })


# ---------------- API HELPER FOR DYNAMIC DROPDOWNS ----------------

@login_required
def api_courses_by_department(request, department_id):
    """Returns JSON of courses belonging to given department for dynamic dropdown updates."""
    courses = Course.objects.filter(department_id=department_id).values('id', 'name', 'code')
    return JsonResponse({'courses': list(courses)})
