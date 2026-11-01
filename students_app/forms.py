from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Department, Course, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'register_number', 'email', 'phone', 
            'gender', 'date_of_birth', 'department', 'course', 
            'year_semester', 'cgpa', 'photo', 'address', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full student name', 'required': True}),
            'register_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. REG2024001', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@institution.edu', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8901', 'required': True}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'department': forms.Select(attrs={'class': 'form-select', 'id': 'id_department', 'required': True}),
            'course': forms.Select(attrs={'class': 'form-select', 'id': 'id_course', 'required': True}),
            'year_semester': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.00', 'max': '10.00', 'placeholder': 'e.g. 8.75', 'required': True}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Permanent residential address (optional)'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate departments and courses nicely
        self.fields['department'].empty_label = "Select Department"
        self.fields['course'].empty_label = "Select Course"
        
        # If department is selected or in POST data, we can optionally scope courses
        if 'department' in self.data:
            try:
                dept_id = int(self.data.get('department'))
                self.fields['course'].queryset = Course.objects.filter(department_id=dept_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department:
            self.fields['course'].queryset = self.instance.department.courses.all()

    def clean_cgpa(self):
        cgpa = self.cleaned_data.get('cgpa')
        if cgpa is not None:
            if cgpa < 0.0 or cgpa > 10.0:
                raise ValidationError("CGPA must be between 0.00 and 10.00.")
        return cgpa


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science & Engineering', 'required': True}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CSE', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description of the department...'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        return code.strip().upper() if code else code


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department', 'credits', 'duration_years', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Tech in Artificial Intelligence', 'required': True}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS201 / BTECH-AI', 'required': True}),
            'department': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30, 'value': 4}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6, 'value': 4}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Course overview and objectives...'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        return code.strip().upper() if code else code


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last Name'
    }))
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Admin/Staff Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password', 'id': 'regPassword'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password', 'id': 'regConfirmPassword'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username or Email Address', 
            'id': 'loginUsername', 
            'autofocus': True,
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password', 
            'id': 'loginPassword',
            'required': True
        })
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input', 'id': 'rememberMe'
    }))
