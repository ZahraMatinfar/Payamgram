from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from hashlib import sha256
from apps.user.forms import RegisterForm, LoginForm
from apps.user.models import User
from django.db.models import Q


class SignIn(View):
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
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
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