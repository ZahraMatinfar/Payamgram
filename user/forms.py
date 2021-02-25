from django import forms
from django.core.exceptions import ValidationError

from django import forms
from apps.user.models import User
from apps.user.validators import minimum_age


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='نام', max_length=100, required=False)
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, required=False)
    email = forms.CharField(label='ایمیل', max_length=200)
    username = forms.CharField(label='نام کاربری', max_length=100)
    password = forms.CharField(label='گذرواژه', max_length=100)
    birthday = forms.DateField(label='تاریخ تولد',
                               widget=forms.TextInput(attrs={'type': 'date'}))

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if minimum_age(birthday):
            return self.cleaned_data['birthday']

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
    email = forms.CharField(label='ایمیل', max_length=200)
    password = forms.CharField(label='گذرواژه', max_length=100)



# class SearchForm(forms.Mfht.TextWidget("PersonAutocomplete"),}