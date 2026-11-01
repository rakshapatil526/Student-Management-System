from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # Module 1: Dashboard
    path('', views.dashboard_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Module 2, 3, 4: Students Management & Search
    path('students/', views.student_list_view, name='student_list'),
    path('students/add/', views.student_create_view, name='student_add'),
    path('students/<int:pk>/', views.student_detail_view, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit_view, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete_view, name='student_delete'),
    path('students/export/csv/', views.export_students_csv, name='export_students_csv'),

    # Module 5: Department & Course Management
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/add/', views.department_create_view, name='department_add'),
    path('departments/<int:pk>/edit/', views.department_edit_view, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete_view, name='department_delete'),

    path('courses/', views.course_list_view, name='course_list'),
    path('courses/add/', views.course_create_view, name='course_add'),
    path('courses/<int:pk>/edit/', views.course_edit_view, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete_view, name='course_delete'),

    # AJAX API
    path('api/departments/<int:department_id>/courses/', views.api_courses_by_department, name='api_courses_by_dept'),
]
