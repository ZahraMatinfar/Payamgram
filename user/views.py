import json
from hashlib import sha256

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView

from apps.user.forms import RegisterForm, LoginForm
from apps.user.models import User


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


class UserList(ListView):  # list of users
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserDetail(DetailView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['post_user'] = User.objects.get_post_user()
        return context


# def autocomplete(request):
#     if 'username' in request.GET:
#         qs = User.objects.filter(username__istartswith=request.GET.get('username'))
#         users = []
#         for user in qs:
#             users.append(user.username)
#         return JsonResponse(users, safe=False)
#         # return HttpResponse(users, safe=False)
#     return render(request, 'user/profile.html')


def autocompletemodel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = User.objects.filter(username__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
