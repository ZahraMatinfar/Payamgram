from hashlib import sha256
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from apps.user.filters import UserFilter
from apps.user.forms import RegisterForm, LoginForm
from apps.user.models import User


class SignIn(View):
    """
    This view is used for sign in.
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/signup.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            user = User(**validated_data)
            user.save()
            return redirect('index')
        return render(request, 'user/signup.html', {'form': form})


class Login(View):
    """
       This view is used for login.
       """
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        """
        Input password after hashing with username will compared with database. If user is in database
        User will redirect to her/his profile.
        :return: render login page
        """
        message = ''
        form = LoginForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            password = sha256(validated_data['password'].encode('utf-8')).hexdigest()
            try:
                user = User.objects.get(email__exact=validated_data['email'], password__exact=password)
            except User.DoesNotExist:
                message = 'نام کاربری یا رمز عبور اشتباه است.'
            else:
                user.login = True
                return redirect('profile', user.slug)
        return render(request, 'user/login.html', {'form': form, 'message': message})


class Profile(DetailView):
    model = User
    template_name = 'user/profile.html'


class UserDetail(DetailView):
    model = User


class UserList(ListView):
    model = User


class FindUser(View):
    """
    by using a custom filter ,user can search to find another users.This view is used for autocomplete search.
    """
    def get(self, request):
        user_filter = UserFilter(request.GET, User.objects.all())
        return render(request, 'user/find_user.html', {'user_filter': user_filter})
