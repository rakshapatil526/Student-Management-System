from django.contrib import admin
from .models import Department, Course, Student


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'credits', 'duration_years')
    list_filter = ('department', 'duration_years')
    search_fields = ('name', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'register_number', 'email', 'department', 'course', 'year_semester', 'cgpa', 'status')
    list_filter = ('department', 'course', 'gender', 'status', 'year_semester')
    search_fields = ('name', 'register_number', 'email', 'phone')
    ordering = ('-created_at',)
