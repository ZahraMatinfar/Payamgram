import os
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from ghasedak import ghasedak

from apps.user.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, CreateView, UpdateView, FormView
from apps.user.filters import UserFilter
from apps.user.forms import RegisterForm, LoginForm, ProfileForm, UserForm, PasswordResetForm
from apps.user.models import Profile
from apps.user.models import UserFollowing
from apps.user.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django_otp.util import random_hex
from .totp import TOTPVerification
import ghasedak


def unique_key():
    """
    :return: create random key to send sms
    """
    key = random_hex(20)
    try:
        User.objects.get(key=key)
    except ObjectDoesNotExist:
        return key
    else:
        unique_key()


class Signup(CreateView):
    """
    classView for signing up
    """
    form_class = RegisterForm
    template_name = 'user/signup.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.key = unique_key()
        self.object.is_active = False
        self.object.save()
        if self.request.POST.get('verifyRadios') == 'email':
            current_site = get_current_site(self.request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user/acc_active_email.html', {
                'user': self.object,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'token': account_activation_token.make_token(self.object),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        elif self.request.POST.get('verifyRadios') == 'sms':
            return redirect('activate_sms', self.object.slug)
        Profile.objects.create(user=self.object)
        return HttpResponse('Please confirm your email address to complete the registration')

    def get_success_url(self):
        return reverse('index')


class Login(View):
    """
    classView for signing in
    """

    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        next = request.GET.get('next')
        message = ''
        if form.is_valid():
            auth_field = form.cleaned_data['auth_field']
            password = form.cleaned_data['password']
            try:
                user_obj = User.objects.get(
                    Q(email__exact=auth_field) | Q(username__exact=auth_field) | Q(mobile__exact=auth_field))
            except ObjectDoesNotExist:
                message = 'There is no such user'
            else:
                user = authenticate(username=user_obj.username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        if next:
                            return redirect(next)
                        else:
                            return redirect('index')
                    else:
                        message = 'User is deactivate'
                else:
                    message = 'email or password is invalid'
        return render(request, 'user/login.html', {'form': form, 'message': message})


class Logout(LoginRequiredMixin, View):
    """
    classView for logging out
    """

    def get(self, request):
        logout(request)
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    """
    personal profile view
    """

    def get(self, request, slug):
        profile_user = User.objects.get(slug=slug)
        login_user = request.user
        return render(request, 'user/profile.html', {'profile_user': profile_user, 'login_user': login_user})

    def post(self, request, slug):

        profile_user = User.objects.get(slug=slug)
        login_user = request.user
        follow = request.POST.get('follow')
        if follow:
            try:
                following = UserFollowing.objects.get(user=login_user, following_user=profile_user)
            except ObjectDoesNotExist:
                if login_user in profile_user.target.requests.all():
                    profile_user.target.requests.remove(login_user)
                else:
                    profile_user.target.requests.add(login_user)
            else:
                following.delete()

            return redirect('profile', profile_user.slug)
        return render(request, 'user/profile.html', {'profile_user': profile_user, 'login_user': login_user})


class FindUser(View):
    """
    by using a custom filter ,user can search to find another users.This view is used for autocomplete search.
    """

    def get(self, request):
        user_filter = UserFilter(request.GET, User.objects.all())
        # user = request.user
        return render(request, 'user/find_user.html', {'user_filter': user_filter})


class ConfirmRequestView(View):
    """
    It will be called if a user confirm someone's request
    """

    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        request.user.target.requests.remove(user)
        UserFollowing.objects.create(user=user, following_user=request.user)
        return redirect('profile', request.user.slug)


class DeleteRequestView(View):
    """
    It will be called if a user delete someone's request
    """

    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        request.user.target.requests.remove(user)
        return redirect('profile', request.user.slug)


class EditUserProfileView(UpdateView):
    """
    updating user profile
    """
    model = Profile
    form_class = ProfileForm
    template_name = "user/edit_profile.html"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.id)

    def get(self, request, *args, **kwargs):
        self.referer = request.META.get("HTTP_REFERER", "")
        request.session["login_referer"] = self.referer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.referer = request.session.get("login_referer", "")
        old_image = self.get_object().image
        clear = self.request.POST.get('image-clear')
        form = self.get_form()
        if form.is_valid():
            new_image = form.cleaned_data['image']
            if old_image and old_image != new_image and clear != 'on':
                os.remove(old_image.path)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile', kwargs={
            'slug': self.object.user.slug,
        })


def change_password(request):
    """
    :return: changing password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!!!!!!!')
            return redirect('profile', request.user.slug)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })


class ActivateView(View):
    """
    classView for activate user
    """
    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')


def autocomplete(request):
    """
    :return: find users automatically
    """
    if 'term' in request.GET:
        qs = User.objects.filter(username__startswith=request.GET.get('term'))
        titles = list()
        for person in qs:
            titles.append(person.username)
        return JsonResponse(titles, safe=False)
    return render(request, 'user/search.html')


class VerifySMS(View):
    """
    classView for sending code to user's mobile
    """
    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        totp_obj = TOTPVerification(user.key)
        generated_token = totp_obj.generate_token()
        sms = ghasedak.Ghasedak("f94866bb4670a2a772fcd7e70d67683716ec16af0c65ce9024326f0c5e94148f")
        sms.send(
            {'message': f"{generated_token}", 'receptor': "09372190740",
             'linenumber': "10008566"})
        # sms.send(
        #     {'message': f"Payamgram Activation code: {generated_token}", 'receptor': f"0{user.mobile[3:]}",
        #      'linenumber': "10008566"})
        return render(request, 'user/acc_active_sms.html', {'user': user})

    def post(self, request, slug):
        user = User.objects.get(slug=slug)
        input_token = request.POST.get('token')
        totp_obj = TOTPVerification(user.key)
        if totp_obj.verify_token(input_token):
            user.is_active = True
            user.save()
            return redirect('login')
        message = 'this code is invalid'
        return render(request, 'user/acc_active_sms.html', {'message': message, 'user': user})


class PasswordResetView(PasswordContextMixin, FormView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset_form.html'
    token_generator = default_token_generator
    title = 'Password reset'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        try:
            user = User.objects.get(phone_number=phone_number)
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'request': self.request,
            }
            form.save(**opts)
        except User.DoesNotExist:
            form.add_error(None, 'There is no such user with this mobile!!')
            return self.form_invalid(form)
        return super().form_valid(form)


class EditUser(UpdateView):
    """
    classView for editing user's account
    """
    model = User
    form_class = UserForm
    template_name = "user/edit_user.html"

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            form.instance.user = None
            return render(self.request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse('profile', kwargs={
            'slug': self.object.user.slug,
        })
