# core/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Content, Enrollment, ReportCard
from datetime import date, timedelta
from django.utils import timezone

# Ottieni il modello utente personalizzato
CustomUser = get_user_model()

class ModelsTestCase(TestCase):
    def setUp(self):
        # Crea utenti
        self.teacher_user = CustomUser.objects.create_user(username='teacher', password='teacherpassword', is_teacher=True)
        self.student_user = CustomUser.objects.create_user(username='student', password='studentpassword', is_student=True)
        self.another_student = CustomUser.objects.create_user(username='anotherstudent', password='anotherpassword', is_student=True)

        # Crea corsi
        self.course1 = Course.objects.create(
            title='Matematica Avanzata',
            description='Corso completo di matematica',
            teacher=self.teacher_user,
            price=99.99,
            difficulty='advanced',
            status='published'
        )
        self.course2 = Course.objects.create(
            title='Introduzione alla Storia',
            description='Panoramica sulla storia mondiale',
            teacher=self.teacher_user,
            price=49.99,
            difficulty='beginner',
            status='draft'
        )

        # Crea lezioni
        self.lesson1_c1 = Lesson.objects.create(course=self.course1, title='Algebra Lineare', order=1)
        self.lesson2_c1 = Lesson.objects.create(course=self.course1, title='Calcolo Differenziale', order=2)

        # Crea contenuti
        self.content1_l1 = Content.objects.create(lesson=self.lesson1_c1, title='Introduzione all\'algebra', content_type='text', text_content='Testo della lezione 1', order=1)
        self.content2_l1 = Content.objects.create(lesson=self.lesson1_c1, title='Video spiegazione', content_type='video', url_content='https://youtube.com/test', order=2)

        # Crea iscrizioni
        self.enrollment1 = Enrollment.objects.create(student=self.student_user, course=self.course1)
        self.enrollment2 = Enrollment.objects.create(student=self.student_user, course=self.course2) # Iscrizione anche a corso draft

        # Crea pagelle
        self.report_card1 = ReportCard.objects.create(
            student=self.student_user,
            course=self.course1,
            score=85.50,
            notes='Ottimo lavoro!',
            date_issued=date.today()
        )
        self.report_card2 = ReportCard.objects.create(
            student=self.student_user,
            course=self.course2,
            score=70.00,
            notes='Può migliorare.',
            date_issued=date.today() - timedelta(days=30)
        )
        self.report_card3 = ReportCard.objects.create(
            student=self.another_student,
            course=self.course1,
            score=92.00,
            notes='Eccellente!',
            date_issued=date.today()
        )

    def test_custom_user_creation(self):
        """Testa la creazione di utenti personalizzati (studente e insegnante)."""
        self.assertTrue(self.teacher_user.is_teacher)
        self.assertFalse(self.teacher_user.is_student)
        self.assertTrue(self.student_user.is_student)
        self.assertFalse(self.student_user.is_teacher)
        self.assertEqual(str(self.teacher_user), 'teacher')

    def test_course_creation(self):
        """Testa la creazione di un corso."""
        self.assertEqual(self.course1.title, 'Matematica Avanzata')
        self.assertEqual(self.course1.teacher, self.teacher_user)
        self.assertEqual(float(self.course1.price), 99.99)
        self.assertTrue(self.course1.is_published) # status='published'

    def test_course_student_count(self):
        """Testa il conteggio degli studenti iscritti a un corso."""
        self.assertEqual(self.course1.student_count, 2) # student_user e another_student

    def test_lesson_creation(self):
        """Testa la creazione di una lezione."""
        self.assertEqual(self.lesson1_c1.course, self.course1)
        self.assertEqual(self.lesson1_c1.title, 'Algebra Lineare')
        self.assertEqual(self.lesson1_c1.order, 1)

    def test_content_creation(self):
        """Testa la creazione di un contenuto."""
        self.assertEqual(self.content1_l1.lesson, self.lesson1_c1)
        self.assertEqual(self.content1_l1.content_type, 'text')
        self.assertEqual(self.content2_l1.url_content, 'https://youtube.com/test')

    def test_enrollment_creation(self):
        """Testa la creazione di un'iscrizione."""
        self.assertEqual(self.enrollment1.student, self.student_user)
        self.assertEqual(self.enrollment1.course, self.course1)
        self.assertFalse(self.enrollment1.completed)

    def test_enrollment_unique_together(self):
        """Testa che uno studente non possa iscriversi due volte allo stesso corso."""
        with self.assertRaises(Exception):
            Enrollment.objects.create(student=self.student_user, course=self.course1)

    def test_report_card_creation(self):
        """Testa la creazione di una pagella e i suoi attributi."""
        self.assertEqual(self.report_card1.student, self.student_user)
        self.assertEqual(self.report_card1.course, self.course1)
        self.assertEqual(float(self.report_card1.score), 85.50)
        self.assertEqual(self.report_card1.notes, 'Ottimo lavoro!')
        self.assertEqual(self.report_card1.date_issued, date.today())
        self.assertEqual(str(self.report_card1), f"Pagella di {self.student_user.username} per {self.course1.title} - Punteggio: 85.50")

    def test_report_card_unique_together(self):
        """Testa che non si possano creare pagelle duplicate per lo stesso studente, corso e data."""
        with self.assertRaises(Exception):
            ReportCard.objects.create(
                student=self.student_user,
                course=self.course1,
                score=90.00,
                date_issued=date.today()
            )

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = CustomUser.objects.create_user(username='studentuser', password='password123', is_student=True)
        self.teacher_user = CustomUser.objects.create_user(username='teacheruser', password='password123', is_teacher=True)
        self.anon_user = CustomUser.objects.create_user(username='anonuser', password='password123') # Utente non studente/insegnante

        self.course_math = Course.objects.create(title='Math', description='Math course', teacher=self.teacher_user, price=100.00)
        self.course_history = Course.objects.create(title='History', description='History course', teacher=self.teacher_user, price=50.00)

        self.report_card_math = ReportCard.objects.create(
            student=self.student_user, course=self.course_math, score=85.00, date_issued=timezone.now().date()
        )
        self.report_card_history = ReportCard.objects.create(
            student=self.student_user, course=self.course_history, score=70.00, date_issued=timezone.now().date() - timedelta(days=10)
        )
        self.report_card_other_student = ReportCard.objects.create(
            student=self.anon_user, course=self.course_math, score=90.00, date_issued=timezone.now().date()
        )

    # --- Test Homepage View ---
    def test_homepage_view(self):
        response = self.client.get(reverse('core:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/homepage.html')
        self.assertContains(response, 'Benvenuto alla Juan Academy!')

    # --- Test Registration View ---
    def test_register_view_get(self):
        response = self.client.get(reverse('core:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Registrati')

    def test_register_view_post_success(self):
        response = self.client.post(reverse('core:register'), {
            'username': 'newuser',
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'new@example.com',
            'is_student': True,
            'is_teacher': False
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/homepage.html')
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())
        self.assertTrue(CustomUser.objects.get(username='newuser').is_student)
        self.assertContains(response, 'Registrazione avvenuta con successo.')


    # --- Test Login View ---
    def test_login_view_get(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Accedi')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'studentuser',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/homepage.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'Sei loggato come studentuser.')

    def test_login_view_post_failure(self):
        response = self.client.post(reverse('core:login'), {
            'username': 'studentuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Username o password non validi.')

    # --- Test Logout View ---
    def test_logout_view(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('core:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/homepage.html')
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Sei stato disconnesso con successo.')

    # --- Test student_report_cards View ---
    def test_student_report_cards_requires_login(self):
        """Test che la vista delle pagelle richiede il login."""
        response = self.client.get(reverse('core:my_report_cards'))
        self.assertRedirects(response, f'{reverse("core:login")}?next={reverse("core:my_report_cards")}')

    def test_student_report_cards_displays_only_own_report_cards(self):
        """Test che la vista mostra solo le pagelle dell'utente loggato."""
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('core:my_report_cards'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/student_report_cards.html')
        self.assertContains(response, self.report_card_math.course.title)
        self.assertContains(response, self.report_card_history.course.title)
        self.assertNotContains(response, self.report_card_other_student.course.title) # Non dovrebbe contenere la pagella di un altro utente

    def test_student_report_cards_empty(self):
        """Test che la vista mostra il messaggio 'non ci sono pagelle' se non ve ne sono."""
        self.client.login(username='teacheruser', password='password123') # Un insegnante non ha pagelle
        response = self.client.get(reverse('core:my_report_cards'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Non ci sono ancora pagelle disponibili per te.')

    # --- Test report_card_detail View ---
    def test_report_card_detail_requires_login(self):
        """Test che la vista dettaglio pagella richiede il login."""
        response = self.client.get(reverse('core:report_card_detail', args=[self.report_card_math.pk]))
        self.assertRedirects(response, f'{reverse("core:login")}?next={reverse("core:report_card_detail", args=[self.report_card_math.pk])}')

    def test_report_card_detail_displays_correct_report_card(self):
        """Test che la vista dettaglio pagella mostra i dettagli corretti."""
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('core:report_card_detail', args=[self.report_card_math.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/report_card_detail.html')
        self.assertContains(response, self.report_card_math.course.title)
        self.assertContains(response, str(self.report_card_math.score))
        self.assertContains(response, self.report_card_math.student.username)

    def test_report_card_detail_prevents_access_to_other_users_report_cards(self):
        """Test che un utente non può accedere alla pagella di un altro utente."""
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('core:report_card_detail', args=[self.report_card_other_student.pk]))
        self.assertEqual(response.status_code, 404) # Dovrebbe dare 404 (Not Found) perché non appartiene all'utente