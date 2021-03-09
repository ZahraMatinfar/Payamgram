from django import forms
from django.contrib.auth.models import User
from apps.user.models import Profile

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'url', 'gender')

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile
