/**
 * Attenda / EduManage Application JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {

    // 1. Password Toggle (Show/Hide Password)
    const toggleButtons = document.querySelectorAll('[data-toggle-password]');
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetInputId = btn.getAttribute('data-toggle-password');
            const targetInput = document.getElementById(targetInputId);
            const icon = btn.querySelector('i');

            if (targetInput) {
                if (targetInput.type === 'password') {
                    targetInput.type = 'text';
                    if (icon) {
                        icon.classList.remove('bi-eye');
                        icon.classList.add('bi-eye-slash');
                    }
                } else {
                    targetInput.type = 'password';
                    if (icon) {
                        icon.classList.remove('bi-eye-slash');
                        icon.classList.add('bi-eye');
                    }
                }
            }
        });
    });

    // 2. Department to Course Dynamic AJAX Cascading Dropdown
    const deptSelect = document.getElementById('id_department');
    const courseSelect = document.getElementById('id_course');

    if (deptSelect && courseSelect) {
        deptSelect.addEventListener('change', async () => {
            const deptId = deptSelect.value;
            if (!deptId) {
                courseSelect.innerHTML = '<option value="">Select Course</option>';
                return;
            }

            try {
                const response = await fetch(`/api/departments/${deptId}/courses/`);
                if (response.ok) {
                    const data = await response.json();
                    let options = '<option value="">Select Course</option>';
                    data.courses.forEach(course => {
                        options += `<option value="${course.id}">${course.name} [${course.code}]</option>`;
                    });
                    courseSelect.innerHTML = options;
                }
            } catch (err) {
                console.error("Error fetching courses for department:", err);
            }
        });
    }

    // 3. Image Upload Preview
    const photoInput = document.querySelector('input[type="file"][name="photo"]');
    const photoPreview = document.getElementById('studentPhotoPreview');

    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    photoPreview.src = event.target.result;
                    photoPreview.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 4. Mobile Sidebar Toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('.app-sidebar');
    const backdrop = document.querySelector('.sidebar-backdrop');

    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
            if (backdrop) backdrop.classList.toggle('show');
        });

        if (backdrop) {
            backdrop.addEventListener('click', () => {
                sidebar.classList.remove('show');
                backdrop.classList.remove('show');
            });
        }
    }

    // 5. Auto dismiss alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            try {
                const bsAlert = bootstrap.Alert.getInstance(alert) || new bootstrap.Alert(alert);
                bsAlert.close();
            } catch(e) {}
        });
    }, 6000);

});
