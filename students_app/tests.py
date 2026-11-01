from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students_app.models import Department, Course, Student
import datetime

class StudentManagementSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Admin User
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin_test@institution.edu',
            password='password123',
            first_name='Admin',
            last_name='Tester'
        )

        # Create Department
        self.dept = Department.objects.create(
            name='Computer Science & Engineering',
            code='CSE',
            description='Test CS Dept'
        )

        # Create Course
        self.course = Course.objects.create(
            name='B.Tech in Artificial Intelligence',
            code='CS-AI-101',
            department=self.dept,
            credits=4,
            duration_years=4
        )

        # Create Student
        self.student = Student.objects.create(
            name='Alice Wonderland',
            register_number='REG-TEST-001',
            email='alice@institution.edu',
            phone='+1 555-1234',
            gender='Female',
            date_of_birth=datetime.date(2003, 5, 20),
            department=self.dept,
            course=self.course,
            year_semester='Year 2 / Semester 3',
            cgpa=9.25,
            status='Active'
        )

    def test_login_with_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_email(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin_test@institution.edu',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_incorrect_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'wrongpassword'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Staff',
            'username': 'newstaff',
            'email': 'newstaff@institution.edu',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newstaff').exists())
        self.assertTrue(response.context['user'].is_authenticated)

    def test_dashboard_view(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_students'], 1)
        self.assertEqual(response.context['total_departments'], 1)
        self.assertEqual(response.context['total_courses'], 1)

    def test_add_student(self):
        self.client.login(username='admin_test', password='password123')
        post_data = {
            'name': 'Bob Smith',
            'register_number': 'REG-TEST-002',
            'email': 'bob@institution.edu',
            'phone': '+1 555-5678',
            'gender': 'Male',
            'date_of_birth': '2004-01-15',
            'department': self.dept.id,
            'course': self.course.id,
            'year_semester': 'Year 1 / Semester 1',
            'cgpa': '8.50',
            'status': 'Active'
        }
        response = self.client.post(reverse('student_add'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Student.objects.filter(register_number='REG-TEST-002').exists())

    def test_student_search_and_filter(self):
        self.client.login(username='admin_test', password='password123')
        # Search by name
        response = self.client.get(reverse('student_list') + '?q=Alice')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 1)

        # Search by non-existent name
        response = self.client.get(reverse('student_list') + '?q=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_student_detail_view(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('student_detail', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice Wonderland')
        self.assertContains(response, 'REG-TEST-001')

    def test_student_edit(self):
        self.client.login(username='admin_test', password='password123')
        post_data = {
            'name': 'Alice W. Updated',
            'register_number': 'REG-TEST-001',
            'email': 'alice.updated@institution.edu',
            'phone': '+1 555-1234',
            'gender': 'Female',
            'date_of_birth': '2003-05-20',
            'department': self.dept.id,
            'course': self.course.id,
            'year_semester': 'Year 2 / Semester 4',
            'cgpa': '9.65',
            'status': 'Active'
        }
        response = self.client.post(reverse('student_edit', kwargs={'pk': self.student.pk}), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Alice W. Updated')
        self.assertEqual(float(self.student.cgpa), 9.65)

    def test_department_deletion_protection_when_linked(self):
        self.client.login(username='admin_test', password='password123')
        # Deletion should be refused because student is enrolled
        response = self.client.post(reverse('department_delete', kwargs={'pk': self.dept.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Department.objects.filter(pk=self.dept.pk).exists())

    def test_export_students_csv(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('export_students_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Alice Wonderland', response.content.decode('utf-8'))
