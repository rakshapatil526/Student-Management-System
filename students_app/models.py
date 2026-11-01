from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True, help_text="Department name (e.g. Computer Science & Engineering)")
    code = models.CharField(max_length=20, unique=True, help_text="Short code (e.g. CSE)")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the department")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_student_count(self):
        return self.students.count()

    def get_course_count(self):
        return self.courses.count()


class Course(models.Model):
    name = models.CharField(max_length=160, help_text="Course title (e.g. B.Tech in Artificial Intelligence)")
    code = models.CharField(max_length=30, unique=True, help_text="Course code (e.g. CS101, BT-AI-204)")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    credits = models.PositiveIntegerField(default=4, help_text="Course credits")
    duration_years = models.PositiveIntegerField(default=4, help_text="Duration in years")
    description = models.TextField(blank=True, null=True, help_text="Overview of the course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.code}]"

    def get_student_count(self):
        return self.students.count()


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    YEAR_SEMESTER_CHOICES = [
        ('Year 1 / Semester 1', 'Year 1 / Semester 1'),
        ('Year 1 / Semester 2', 'Year 1 / Semester 2'),
        ('Year 2 / Semester 3', 'Year 2 / Semester 3'),
        ('Year 2 / Semester 4', 'Year 2 / Semester 4'),
        ('Year 3 / Semester 5', 'Year 3 / Semester 5'),
        ('Year 3 / Semester 6', 'Year 3 / Semester 6'),
        ('Year 4 / Semester 7', 'Year 4 / Semester 7'),
        ('Year 4 / Semester 8', 'Year 4 / Semester 8'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
    ]

    name = models.CharField(max_length=150, help_text="Full Name of the student")
    register_number = models.CharField(max_length=50, unique=True, help_text="Unique Registration / Roll Number")
    email = models.EmailField(unique=True, help_text="Student's email address")
    phone = models.CharField(max_length=25, help_text="Contact number")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    date_of_birth = models.DateField(help_text="Date of birth")
    
    # Linked to Department & Course
    # on_delete=models.PROTECT prevents deleting department/course while students exist!
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='students')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='students')
    
    year_semester = models.CharField(max_length=50, choices=YEAR_SEMESTER_CHOICES, default='Year 1 / Semester 1')
    cgpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Cumulative Grade Point Average (0.00 - 10.00)"
    )
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True, help_text="Optional profile photo")
    address = models.TextField(blank=True, null=True, help_text="Permanent / Residential address")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.register_number})"

    @property
    def cgpa_badge_class(self):
        if self.cgpa >= 8.5:
            return 'bg-success text-white'
        elif self.cgpa >= 7.0:
            return 'bg-primary text-white'
        elif self.cgpa >= 5.0:
            return 'bg-warning text-dark'
        else:
            return 'bg-danger text-white'
