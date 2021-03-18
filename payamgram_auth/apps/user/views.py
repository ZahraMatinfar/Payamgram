from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.user.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.views.generic import View, CreateView, UpdateView
from apps.user.filters import UserFilter
from apps.user.forms import RegisterForm, LoginForm, UserProfileForm
from apps.user.models import Profile
from apps.user.models import UserFollowing
from apps.user.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class Singing(CreateView):
    form_class = RegisterForm
    template_name = 'user/signing.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
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
        # super().form_valid(form)
        Profile.objects.create(user=self.object)
        # login(self.request, self.object)
        return HttpResponse('Please confirm your email address to complete the registration')

    def get_success_url(self):
        return reverse('index')


class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        next = request.GET.get('next')
        message = ''
        if form.is_valid():
            email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user = authenticate(username=email, password=password)
            # if user:
            #     if user.is_active:
            #         login(request, user)
            #         if next:
            #             return redirect(next)
            #         else:
            #             return redirect('index')
            #     else:
            #         message = 'User is deactivate'
            # else:
            #     message = 'email or password is invalid'
            try:
                user_obj = User.objects.get(email__exact=email)
            except ObjectDoesNotExist:
                message = 'email or password is invalid'
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
        # print('...',profile_user.target.requests.all())
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
        return render(request, 'user/find_user.html', {'user_filter': user_filter})


class ConfirmRequestView(View):
    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        request.user.target.requests.remove(user)
        UserFollowing.objects.create(user=user, following_user=request.user)
        return redirect('profile', request.user.slug)


class DeleteRequestView(View):
    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        request.user.target.requests.remove(user)
        return redirect('profile', request.user.slug)


class EditUserProfileView(UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = "user/user_profile.html"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.id)

    def get(self, request, *args, **kwargs):
        self.referer = request.META.get("HTTP_REFERER", "")
        request.session["login_referer"] = self.referer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.referer = request.session.get("login_referer", "")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile', kwargs={
            'slug': self.object.user.slug,
        })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', request.user.slug)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })


class ActivateView(View):
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
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
