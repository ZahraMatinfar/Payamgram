from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    """
    a form for sig in.
    """

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        # widgets = {
        #     'birthday': forms.TextInput(attrs={'type': 'date'}),
        # }
        # labels = {
        #     'first_name': 'نام',
        #     'last_name': 'نام خانوادگی',
        #     'email': 'ایمیل',
        #     'username': 'نام کاربری',
        #     'password': 'گذرواژه',
        # }

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     user = User.objects.filter(username__exact=username)
    #     if user:
    #         raise ValidationError('این نام کاربری قبلا ثبت شده است.')
    #     else:
    #         return self.cleaned_data['username']
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     user = User.objects.filter(email__exact=email)
    #     if user:
    #         raise ValidationError('این ایمیل قبلا ثبت شده است.')
    #     else:
    #         return self.cleaned_data['email']


class LoginForm(forms.Form):
    """
        a form for sig in.
    """
    # email = forms.EmailField( max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'password'}))
