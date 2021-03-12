from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.user.models import Profile


class RegisterForm(UserCreationForm):
    """
    a form for sig in.
    """

    class Meta:
        model = User
        fields = ['email', 'username']
        # widgets = {
        #     'password': forms.TextInput(attrs={'type': 'password'}),
        # }


class LoginForm(forms.Form):
    """
        a form for sig in.
    """
    email = forms.EmailField(max_length=200)
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'password'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'url', 'gender', 'mobile', 'image')

    def save(self, user=None):
        user_profile = super().save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile
