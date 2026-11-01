from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students_app.models import Department, Course, Student
import datetime

class Command(BaseCommand):
    help = 'Seeds initial departments, courses, students, and admin user'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Create Default Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@institution.edu',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Departments
        departments_data = [
            {
                'name': 'Computer Science & Engineering',
                'code': 'CSE',
                'description': 'Pioneering innovation in artificial intelligence, computer architecture, algorithms, and cloud systems.'
            },
            {
                'name': 'Information Technology',
                'code': 'IT',
                'description': 'Focusing on distributed software development, cybersecurity, database architecture, and web systems.'
            },
            {
                'name': 'Electronics & Communication',
                'code': 'ECE',
                'description': 'Specializing in VLSI design, wireless signal processing, embedded IoT systems, and robotics.'
            },
            {
                'name': 'Mechanical Engineering',
                'code': 'MECH',
                'description': 'Design, robotics, thermal sciences, additive manufacturing, and automated industrial machinery.'
            },
            {
                'name': 'School of Management Studies',
                'code': 'MBA',
                'description': 'Developing leaders in tech management, digital marketing, supply chain, and data-driven finance.'
            },
        ]

        depts = {}
        for d in departments_data:
            dept_obj, _ = Department.objects.get_or_create(
                code=d['code'],
                defaults={'name': d['name'], 'description': d['description']}
            )
            depts[d['code']] = dept_obj

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(depts)} departments."))

        # 3. Courses
        courses_data = [
            {'name': 'B.Tech in Artificial Intelligence & Data Science', 'code': 'CS-AI-101', 'dept': 'CSE', 'credits': 4, 'duration_years': 4},
            {'name': 'B.Tech in Computer Science & Engineering', 'code': 'CSE-CORE-201', 'dept': 'CSE', 'credits': 4, 'duration_years': 4},
            {'name': 'B.Tech in Software Systems & Cloud Computing', 'code': 'IT-CLOUD-301', 'dept': 'IT', 'credits': 4, 'duration_years': 4},
            {'name': 'B.Tech in Cyber Security & Forensics', 'code': 'IT-CYBER-302', 'dept': 'IT', 'credits': 4, 'duration_years': 4},
            {'name': 'B.Tech in VLSI & Embedded Systems', 'code': 'ECE-VLSI-401', 'dept': 'ECE', 'credits': 4, 'duration_years': 4},
            {'name': 'B.Tech in Robotics & Mechatronics', 'code': 'MECH-ROBO-501', 'dept': 'MECH', 'credits': 4, 'duration_years': 4},
            {'name': 'MBA in Technology Management', 'code': 'MBA-TECH-601', 'dept': 'MBA', 'credits': 3, 'duration_years': 2},
        ]

        courses = {}
        for c in courses_data:
            course_obj, _ = Course.objects.get_or_create(
                code=c['code'],
                defaults={
                    'name': c['name'],
                    'department': depts[c['dept']],
                    'credits': c['credits'],
                    'duration_years': c['duration_years'],
                    'description': f"Comprehensive curriculum covering core principles of {c['name']}."
                }
            )
            courses[c['code']] = course_obj

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(courses)} courses."))

        # 4. Students
        students_data = [
            {
                'name': 'Alexander Wright',
                'register_number': 'REG2024001',
                'email': 'alexander.wright@institution.edu',
                'phone': '+1 (555) 234-8901',
                'gender': 'Male',
                'dob': datetime.date(2003, 4, 15),
                'dept': 'CSE',
                'course': 'CS-AI-101',
                'year_sem': 'Year 2 / Semester 4',
                'cgpa': 9.45,
                'address': '742 Evergreen Terrace, Springfield, OR',
                'status': 'Active'
            },
            {
                'name': 'Sophia Chen',
                'register_number': 'REG2024002',
                'email': 'sophia.chen@institution.edu',
                'phone': '+1 (555) 345-6712',
                'gender': 'Female',
                'dob': datetime.date(2004, 8, 22),
                'dept': 'CSE',
                'course': 'CSE-CORE-201',
                'year_sem': 'Year 1 / Semester 2',
                'cgpa': 8.90,
                'address': '108 Beacon Hill Road, Boston, MA',
                'status': 'Active'
            },
            {
                'name': 'Marcus Vance',
                'register_number': 'REG2024003',
                'email': 'marcus.vance@institution.edu',
                'phone': '+1 (555) 872-1144',
                'gender': 'Male',
                'dob': datetime.date(2002, 11, 3),
                'dept': 'IT',
                'course': 'IT-CYBER-302',
                'year_sem': 'Year 3 / Semester 6',
                'cgpa': 7.82,
                'address': '55 Elm Street, Austin, TX',
                'status': 'Active'
            },
            {
                'name': 'Emily Rodriguez',
                'register_number': 'REG2024004',
                'email': 'emily.rodriguez@institution.edu',
                'phone': '+1 (555) 432-9090',
                'gender': 'Female',
                'dob': datetime.date(2003, 1, 19),
                'dept': 'IT',
                'course': 'IT-CLOUD-301',
                'year_sem': 'Year 2 / Semester 3',
                'cgpa': 9.12,
                'address': '224 Mission Bay Blvd, San Francisco, CA',
                'status': 'Active'
            },
            {
                'name': 'David Kim',
                'register_number': 'REG2024005',
                'email': 'david.kim@institution.edu',
                'phone': '+1 (555) 678-3321',
                'gender': 'Male',
                'dob': datetime.date(2002, 6, 30),
                'dept': 'ECE',
                'course': 'ECE-VLSI-401',
                'year_sem': 'Year 3 / Semester 5',
                'cgpa': 6.85,
                'address': '890 Sunset Blvd, Los Angeles, CA',
                'status': 'Active'
            },
            {
                'name': 'Olivia Taylor',
                'register_number': 'REG2024006',
                'email': 'olivia.taylor@institution.edu',
                'phone': '+1 (555) 901-5544',
                'gender': 'Female',
                'dob': datetime.date(2001, 9, 12),
                'dept': 'MECH',
                'course': 'MECH-ROBO-501',
                'year_sem': 'Year 4 / Semester 8',
                'cgpa': 8.65,
                'address': '312 Lakeview Avenue, Chicago, IL',
                'status': 'Active'
            },
            {
                'name': 'Aarav Patel',
                'register_number': 'REG2024007',
                'email': 'aarav.patel@institution.edu',
                'phone': '+1 (555) 789-2231',
                'gender': 'Male',
                'dob': datetime.date(2004, 3, 27),
                'dept': 'CSE',
                'course': 'CS-AI-101',
                'year_sem': 'Year 1 / Semester 1',
                'cgpa': 7.40,
                'address': '450 University Circle, Seattle, WA',
                'status': 'Active'
            },
            {
                'name': 'Chloe Bennett',
                'register_number': 'REG2024008',
                'email': 'chloe.bennett@institution.edu',
                'phone': '+1 (555) 321-4455',
                'gender': 'Female',
                'dob': datetime.date(2000, 12, 14),
                'dept': 'MBA',
                'course': 'MBA-TECH-601',
                'year_sem': 'Year 2 / Semester 4',
                'cgpa': 9.60,
                'address': '12 Madison Square, New York, NY',
                'status': 'Active'
            },
        ]

        for s in students_data:
            Student.objects.get_or_create(
                register_number=s['register_number'],
                defaults={
                    'name': s['name'],
                    'email': s['email'],
                    'phone': s['phone'],
                    'gender': s['gender'],
                    'date_of_birth': s['dob'],
                    'department': depts[s['dept']],
                    'course': courses[s['course']],
                    'year_semester': s['year_sem'],
                    'cgpa': s['cgpa'],
                    'address': s['address'],
                    'status': s['status']
                }
            )

        self.stdout.write(self.style.SUCCESS(f"Loaded sample students."))
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
