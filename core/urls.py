# core/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Per le viste di autenticazione predefinite di Django

app_name = 'core' # Molto importante per i reverse lookups (es. {% url 'core:homepage' %})

urlpatterns = [
    path('', views.homepage, name='homepage'), # Homepage
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:homepage'), name='logout'), # Reindirizza alla homepage dopo il logout

    # Dashboard utente
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # URL per la creazione di un corso (solo per insegnanti) - Aggiunto per completezza
    path('courses/create/', views.create_course, name='create_course'),

    # Lista di tutti i corsi (più generale, va dopo i dettagli specifici)
    path('courses/', views.CourseListView.as_view(), name='course_list'),

    # Dettaglio corso (più specifico, va prima della lista generale)
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:pk>/enrolled_students/', views.enrolled_students_view, name='enrolled_students'), # Aggiunto per completezza
    path('courses/<int:pk>/manage_content/', views.manage_course_content, name='manage_course_content'), # Aggiunto per completezza

    # URL per i corsi a cui lo studente è iscritto
    path('my_courses/', views.enrolled_courses_view, name='enrolled_courses'),
]