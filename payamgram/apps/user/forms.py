from django import forms
from django.core.exceptions import ValidationError
from apps.user.models import User


class RegisterForm(forms.ModelForm):
    """
    a form for sig in.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'birthday']
        widgets = {
            'birthday': forms.TextInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'username': 'نام کاربری',
            'password': 'گذرواژه',
            'birthday': 'تاریخ تولد',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username__exact=username)
        if user:
            raise ValidationError('این نام کاربری قبلا ثبت شده است.')
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__exact=email)
        if user:
            raise ValidationError('این ایمیل قبلا ثبت شده است.')
        else:
            return self.cleaned_data['email']


class LoginForm(forms.Form):
    """
        a form for sig in.
    """
    email = forms.CharField(label='ایمیل', max_length=200)
    password = forms.CharField(label='گذرواژه', max_length=100)
