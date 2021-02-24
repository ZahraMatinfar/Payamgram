from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from apps.post.models import Post
from apps.user.forms import CustomUserCreationForm
from apps.user.models import User


def register(request):  # register form
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': f})


class UserList(ListView):  # list of users
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserDetail(DetailView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = User.objects.get_post_user()
        return context













