# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import DetailView, ListView # Non serve CreateView qui se usi una funzione view
from django.urls import reverse_lazy # Non serve se non usi CreateView o UpdateView basate su classi
from .models import CustomUser, Course, Enrollment # Assicurati di aver importato tutti i tuoi modelli
from .forms import CourseForm # Assicurati di aver creato questo form

# Funzione per verificare se l'utente è uno studente
def is_student_check(user):
    return user.is_authenticated and user.is_student()

# Funzione per verificare se l'utente è un insegnante
def is_teacher_check(user):
    return user.is_authenticated and user.is_teacher()

# --- Viste di base ---

def homepage(request):
    """
    Vista per la homepage del sito.
    """
    return render(request, 'core/homepage.html')

def register_view(request):
    """
    Vista per la registrazione di nuovi utenti.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Puoi aggiungere logica qui per assegnare un tipo di utente predefinito
            # ad esempio, user.user_type = 'student'
            user.save()
            messages.success(request, 'Account creato con successo! Ora puoi effettuare il login.')
            return redirect('core:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Dashboard Utente ---

@login_required
@user_passes_test(is_student_check, login_url='core:login') # Reindirizza al login se non studente
def student_dashboard(request):
    """
    Dashboard per gli studenti, mostra i corsi a cui sono iscritti.
    """
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    context = {
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'core/student_dashboard.html', context)

@login_required
@user_passes_test(is_teacher_check, login_url='core:login') # Reindirizza al login se non insegnante
def teacher_dashboard(request):
    """
    Dashboard per gli insegnanti, mostra i corsi che hanno creato.
    """
    my_courses = Course.objects.filter(teacher=request.user)
    context = {
        'my_courses': my_courses
    }
    return render(request, 'core/teacher_dashboard.html', context)

# --- Viste relative ai Corsi ---

class CourseListView(ListView):
    """
    Vista basata su classe per visualizzare una lista di tutti i corsi disponibili.
    """
    model = Course
    template_name = 'core/course_list.html' # Assicurati di creare questo template
    context_object_name = 'courses' # Il nome della variabile nel template (es. {% for course in courses %})

class CourseDetailView(DetailView):
    """
    Vista basata su classe per visualizzare i dettagli di un singolo corso.
    """
    model = Course
    template_name = 'core/course_detail.html' # Assicurati di creare questo template
    context_object_name = 'course' # Il nome della variabile nel template (es. {{ course.title }})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if self.request.user.is_authenticated and self.request.user.is_student():
            context['is_enrolled'] = Enrollment.objects.filter(student=self.request.user, course=course).exists()
        else:
            context['is_enrolled'] = False
        return context


@login_required
@user_passes_test(is_student_check, login_url='core:login')
def enroll_course(request, pk):
    """
    Vista per iscrivere uno studente a un corso.
    """
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            Enrollment.objects.create(student=request.user, course=course)
            messages.success(request, f'Ti sei iscritto con successo al corso "{course.title}"!')
        else:
            messages.info(request, f'Sei già iscritto al corso "{course.title}".')
        return redirect('core:course_detail', pk=pk)
    # Se la richiesta non è POST, potresti voler mostrare una pagina di conferma
    return render(request, 'core/enroll_confirm.html', {'course': course})

@login_required
@user_passes_test(is_teacher_check, login_url='core:login')
def create_course(request):
    """
    Vista per permettere agli insegnanti di creare nuovi corsi.
    Richiede un CourseForm.
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user # Assegna l'insegnante corrente
            course.save()
            messages.success(request, f'Corso "{course.title}" creato con successo!')
            return redirect('core:teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'core/create_course.html', {'form': form})

@login_required
@user_passes_test(is_student_check, login_url='core:login')
def enrolled_courses_view(request):
    """
    Vista per gli studenti per vedere tutti i corsi a cui sono iscritti.
    """
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    context = {
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'core/enrolled_courses.html', context)

@login_required
@user_passes_test(is_teacher_check, login_url='core:login')
def enrolled_students_view(request, pk):
    """
    Vista per gli insegnanti per vedere gli studenti iscritti a un loro corso specifico.
    """
    # Correzione: pk=pk e chiusura della parentesi
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    context = {
        'course': course,
        'enrollments': enrollments
    }
    return render(request, 'core/enrolled_students.html', context)

@login_required
@user_passes_test(is_teacher_check, login_url='core:login')
def manage_course_content(request, pk):
    """
    Vista per gli insegnanti per gestire il contenuto di un corso (es. aggiungere lezioni).
    """
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    # Qui potresti aggiungere la logica per listare/aggiungere lezioni
    messages.info(request, f'Gestione contenuto per il corso: {course.title}')
    return render(request, 'core/manage_course_content.html', {'course': course})