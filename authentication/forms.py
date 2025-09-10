from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password', widget= forms.PasswordInput, required=True)
    password2 = forms.CharField(label = 'Confirm Password', widget= forms.PasswordInput, required=True)
    class Meta: 
        model = User
        fields = ["username", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        else:
            try: 
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data["password1"]

        if password1:
            try: 
                validate_password(password1)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

        return password1
    


    def clean(self):
        cleaned = super().clean()

        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')

        if password1 and password2 and password1 != password2: 
            self.add_error("password2", "Second password doesn't match with first password")

        return cleaned
        


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Your username', required=True, max_length=150)   
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput, required=True)

    def clean(self):
        cleared = super().clean()
        password = cleared.get('password')

        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError({"password": e.messages})

        return cleared

