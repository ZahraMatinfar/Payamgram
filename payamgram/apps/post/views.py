from django.shortcuts import render
from django.views.generic import ListView,DetailView

from apps.post.models import Post
from apps.user.models import User


class PostList(ListView):  # list of posts
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostDetail(DetailView):  # detail of posts
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

