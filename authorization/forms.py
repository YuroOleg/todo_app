from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm


class UserCreationForm(BaseUserCreationForm):
    """Form for user creating"""
    class Meta:
        model = User
        fields = ['email', 'username']


class UserChangeForm(BaseUserChangeForm):
    """Form for user changing"""
    class Meta: 
        model = User
        fields = ['email', 'username', 'is_staff', 'is_active']


class RegisterForm(UserCreationForm):
    """User registration form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this Email already exists.")
        
        return email

class LoginForm(forms.Form):
    """User login form"""
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()

    def clean(self):
        cleaned = super().clean()

        email = cleaned.get('email')
        password = cleaned.get('password')

        if email and password:
            user = authenticate(email = email, password = password)
            if user is None:
                self.add_error('password', ValidationError("Provided email or password is incorrect"))
            self.user = user
        
        return cleaned


            
