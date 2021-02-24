from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView

from apps.post.forms import PostForm
from apps.post.models import Post
from apps.user.models import User


class CreatePost(View):
    def get(self, request, user_slug):
        form = PostForm()
        return render(request, 'post/create_post.html', {'form': form})

    def post(self, request, user_slug):
        form = PostForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username__exact=user_slug)
            validated_data = form.cleaned_data
            post = Post(**validated_data, user=user)
            post.save()
            return redirect('profile', user_slug)
        return render(request, 'post/create_post.html', {'form': form})


class PostList(ListView):
    model = Post


class PostDetail(DetailView):
    model = Post
