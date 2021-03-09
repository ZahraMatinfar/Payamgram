from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, DetailView, CreateView

from django.views.generic import FormView
from django.views.generic import UpdateView
from .filters import UserFilter
from .forms import RegisterForm, LoginForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import Profile
from .models import UserFollowing

class Singing(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/signing.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            user = User.objects.create_user(**validated_data)
            user.save()
            Profile.objects.create(user=user).save()
            return redirect('login')
        return render(request, 'user/signing.html', {'form': form})


# class Singing(CreateView):
#     model = User
#     form_class = RegisterForm
#     template_name = 'user/signing.html'
#     success_url = redirect('login')
#
#     def form_valid(self, form):
#         validated_data = form.cleaned_data
#         user = User.objects.create_user(**validated_data)
#         user.save()
#         return super().form_valid(form)

class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        next = request.GET.get('next')
        message = ''
        if form.is_valid():
            # email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # message = 'Login was successful'
                    if next:
                        return redirect(next)
                    else:
                        return redirect('index')
                else:
                    message = 'User is deactivate'
            else:
                message = 'username or password is invalid'
        return render(request, 'user/login.html', {'form': form, 'message': message})


class Logout(View):
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
        if follow is not None:
            try:
                following = UserFollowing.objects.get(user=login_user, following_user=profile_user)
            except ObjectDoesNotExist:
                UserFollowing.objects.create(user=login_user, following_user=profile_user).save()
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
        # self.success_url = request.session['login_referer']
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
            return redirect('profile',request.user.slug)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })
