import os

from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from ghasedak import ghasedak

from apps.user.models import User
from django.utils.translation import gettext_lazy as _
from apps.user.models import Profile
from apps.user.totp import TOTPVerification


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
        fields = ['first_name', 'last_name', 'email', 'username', 'mobile']
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
    auth_field = forms.CharField(max_length=200,
                                 widget=forms.TextInput(attrs={'placeholder': 'Email or Username or Mobile'}),
                                 required=True)
    password = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'Password'}),
                               required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profile
        fields = ('bio', 'url', 'gender', 'image')
        # widgets={
        #     'image':forms.FileInput()
        # }

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


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'mobile']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile like +9891111111111'})
        }


class PasswordResetForm(forms.Form):
    phone_number = forms.CharField(label=_('mobile'), max_length=11,
                                   validators=[RegexValidator(regex=r'+98(\d{9})$')])

    def send_sms(self, phone_number, reset_link):
        sms = ghasedak.Ghasedak("80676683d3ea3adb452621ec7745a697d4265c609ce9c13c810d34f23add946a")
        sms.send(
            {'message': f"{reset_link}", 'receptor': "09169628133",
             'linenumber': "10008566"})
        # try:
        #     api = kavenegar.KavenegarAPI(settings.KAVENEGAR_APIKEY)
        #     message = f'برای بازیابی رمز عبور روی لینک زیر کلیک کنید \n {reset_link}'
        #     params = {
        #         'sender': '1000596446',
        #         'receptor': phone_number,
        #         'message': message,
        #     }
        #     response = api.sms_send(params)
        #     print(response)
        # except kavenegar.APIException as e:
        #     print(e)
        # except kavenegar.HTTPException as e:
        #     print(e)

    def get_users(self, phone_number):
        return User.objects.get(phone_number=phone_number)

    def save(self, domain_override=None,
             use_https=False, token_generator=default_token_generator,
             request=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        phone_number = self.cleaned_data["phone_number"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        user = self.get_users(phone_number)
        user_phone_number = user.phone_number
        protocol = 'https' if use_https else 'http'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        reset_link = protocol + '://' + domain + reverse('password_reset_confirm',
                                                         args=[uid, token])
        print(reset_link)
        self.send_sms(user_phone_number, reset_link)
