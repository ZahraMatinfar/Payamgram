import os

from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from apps.user.models import User

from apps.user.models import Profile


class RegisterForm(UserCreationForm):
    """
    a form for sig in.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','mobile']
        error_css_class = "error"
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile like +9891111111111'})
        }


class LoginForm(forms.Form):
    """
        a form for sig in.
    """
    auth_field = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email or Username or Mobile'}), required=True)
    password = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password'}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'url', 'gender', 'image')

    def save(self, user=None):
        user_profile = super().save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

    def clean(self):
        cleaned_data = super().clean()
        user_profile = super().save(commit=False)

        if not cleaned_data['image']:
            os.remove(user_profile.image.path)
        return cleaned_data
