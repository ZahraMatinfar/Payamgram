from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.Form):
    first_name = forms.CharField(label='first name', min_length=4, max_length=150)
    last_name = forms.CharField(label='last name', min_length=4, max_length=150)
    birthday = forms.CharField(label='birthday')
    username = forms.CharField(label='Username', min_length=4, max_length=150)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2