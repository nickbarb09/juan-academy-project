# C:\Users\Admin\PyCharmMiscProject\core\forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Course

# --- User Registration Form ---
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Use 'is_student', 'is_teacher', and 'bio' which exist in your CustomUser model.
        # 'username' and 'email' are already handled by UserCreationForm.
        fields = ('username', 'email', 'is_student', 'is_teacher', 'bio')

    def clean(self):
        cleaned_data = super().clean()
        is_student = cleaned_data.get('is_student')
        is_teacher = cleaned_data.get('is_teacher')

        if not is_student and not is_teacher:
            raise forms.ValidationError(
                "Devi selezionare almeno un tipo di utente: Studente o Insegnante."
            )
        return cleaned_data


# --- User Login Form ---
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email o Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# --- Course Creation/Update Form ---
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'price', 'start_date', 'end_date',
            'difficulty', 'status', 'category', 'image'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }