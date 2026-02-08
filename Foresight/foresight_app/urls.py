from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),
    path('contact_from_home/', views.contact_from_home, name='contact_from_home'),
    path('toggle-replied/', views.toggle_replied, name='toggle_replied'),  # ✅
    path('our_team/', views.our_team, name='our_team'),
    path('learning_modules/', views.learning_modules, name='learning_modules'),
    path('bakery_courses/', views.bakery, name='bakery_courses'),
    path('register/', views.student_registration_view, name='register'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('log_out/', views.logout_user, name='log_out'),
    path('credit/', views.credit, name='credit'),

    path('export/', views.export_students_csv, name='export_csv'),
    # path('export-pdf/', views.export_students_pdf, name='export_pdf'),
    path('admin_reg/', views.register_user, name='admin_reg'),
    path('admin_login/', views.login_user, name='admin_login'),
    path('admin_forget/', views.admin_forget, name='admin_forget'),
    path('export_enquiries_csv/', views.export_enquiries_csv, name='export_enquiries_csv'),
    path('export_enquiries_pdf/', views.export_enquiries_pdf, name='export_enquiries_pdf'),



    path('all_students/', views.view_students, name='all_students'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/details/<int:student_id>/', views.student_details_json, name='student_details_json'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),



    path('set_student_passwords/', views.set_student_passwords, name='set_student_passwords'),
    path('posts/', views.view_post, name='posts'),
    path('enquiries/', views.view_enquiries, name='enquiries'),
    path('update-replied/<int:pk>/', views.update_replied, name='update_replied'),
    path('get-enquiry/<int:pk>/', views.get_enquiry, name='get_enquiry'),

    path('privacy/', views.view_privacy_policy, name='privacy'),
    path('add_privacy_policy/', views.add_privacy_policy, name='add_privacy_policy'),
    path('edit_privacy_policy/<int:pk>/', views.edit_privacy_policy, name='edit_privacy_policy'),
    path('delete_privacy_policy/<int:pk>/', views.delete_privacy_policy, name='delete_privacy_policy'),
    path('add_post/', views.post_create, name='post_create'),
    path('edit_post/<int:pk>/', views.post_edit, name='post_edit'),
    path('delete_post/<int:pk>/', views.post_delete, name='post_delete'),
    path('class/', views.view_class, name='class'),
    path('students_in_class/<int:class_id>/', views.students_in_class, name='students_in_class'),
    path('add_class/', views.add_class, name='add_class'),
    path('edit_class/<int:pk>/', views.edit_class, name='edit_class'),
    path('delete_class/<int:pk>/', views.delete_class, name='delete_class'),
    path('staff/', views.staff_management, name='staff_management'),
    path('save-staff/', views.create_or_update_staff, name='create_or_update_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),



    path('admission/', views.admission, name='admission'),
 

    path('base_dash/', views.base_dash, name='base_dash'),
    path('login_staff/', views.login_staff, name='login_staff'),
    # path('forget_staff/', views.forget_staff, name='forget_staff'),
    path('logout_staff/', views.logout_staff, name='logout_staff'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('assign_students_toclass/', views.assign_students_toclass, name='assign_students_toclass'),
    path('manage-admissions/', views.manage_admissions, name='manage_admissions'),
    path('students/<int:class_id>/', views.Students, name='students'),
    path('save-attendance/', views.save_attendance, name='save_attendance'),
    path('get-attendance/', views.get_attendance, name='get_attendance'),

    path('login_student/', views.login_student, name='login_student'),
    path('logout_student/', views.logout_student, name='logout_student'),
    path('student/dashboard/', views.student_attendance_view, name='student_dashboard'),

    path('all_classes/', views.all_classes, name='all_classes'),
    path('attendance/class/<int:class_id>/', views.view_class_attendance, name='view_class_attendance')


    


]
