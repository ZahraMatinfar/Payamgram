import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic import View, CreateView
from .forms import PostForm, CommentForm, PostUpdateForm
from .models import Comment
from .models.post import Post


class CreatePost(LoginRequiredMixin, CreateView):
    """
    view of creating post
    """
    model = Post
    template_name = 'post/create_post.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)  # ?
        if form.is_valid():
            if form.cleaned_data['caption'] == '' and form.cleaned_data['image'] is None:
                message = 'post should contain text or an image!!'
                return render(request, 'post/create_post.html', {'message': message, 'form': form})
            else:
                validated_data = form.cleaned_data
                Post.objects.create(**validated_data, user=request.user)

            return redirect('profile', request.user.slug)
        return render(request, 'post/create_post.html')


class PostDetail(View):
    """
    classView for detail of post
    """

    def get(self, request, slug):
        form = CommentForm()
        post_obj = Post.objects.get(slug=slug)
        return render(request, 'post/post_detail.html', {'form': form, 'object': post_obj})

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post_obj = Post.objects.get(slug=slug)

        if form.is_valid():
            if form.cleaned_data['context']:
                Comment.objects.create(user=request.user, post=post_obj, context=form.cleaned_data['context'])

        return redirect('post_detail', slug)


class DeleteComment(View):
    """
    classView for deleting comment
    """

    @staticmethod
    def get(request, pk):
        comment = Comment.objects.get(id=pk)
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', post_slug)


class EditPost(LoginRequiredMixin, UpdateView):
    """
        updateView for update or changing the post
    """
    model = Post
    template_name = 'post/post_update.html'
    form_class = PostUpdateForm

    def form_valid(self, form):
        if form.cleaned_data['caption'] == '' and form.cleaned_data['image'] is None:
            message = 'post should contain text or an image!!'
            return render(self.request, 'post/post_update.html', {'message': message, 'form': form})
        else:
            form.instance.user = self.request.user
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={
            'slug': self.object.slug,
        })

    def post(self, request, *args, **kwargs):
        """
        for removing unuseful image in media folder ,post function has been overridden.
         old_image: image of post before running of post func
         clear:value of clear check box
         new_image: image of post after editing
        :return: functions of form
        """
        clear = self.request.POST.get('image-clear')
        object = self.get_object()
        old_image = object.image
        if clear == 'on':
            os.remove(object.image.path)
        form = self.get_form()
        if form.is_valid():
            new_image = form.cleaned_data['image']
            if old_image and old_image != new_image and clear != 'on':
                os.remove(old_image.path)
        return super().post(request, *args, **kwargs)


class DeletePost(View):
    """
    classView for deleting a post
    """

    @staticmethod
    def get(request, slug):
        post = Post.objects.get(slug=slug)
        user_slug = post.user.slug
        post.delete()
        return redirect('profile', user_slug)


class LikePost(View):
    """
    classView for liking each post, It checks if user has liked before or not
    """

    def get(self, request, slug):
        post_obj = Post.objects.get(slug=slug)
        likes = post_obj.likes.all()
        if request.user in likes:
            post_obj.likes.remove(request.user)
        else:
            post_obj.likes.add(request.user)
        post_obj.save()
        return redirect('post_detail', slug)
