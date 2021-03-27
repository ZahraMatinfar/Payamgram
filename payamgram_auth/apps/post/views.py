from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, UpdateView

from apps.post.forms import PostForm, CommentForm, PostUpdateForm
from apps.post.models import Post, Comment


class CreatePost(LoginRequiredMixin, CreateView):
    """
    view of creating post
    """
    model = Post
    template_name = 'post/create_post.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if (form.cleaned_data['title'] == '' or form.cleaned_data['caption'] == '') and \
                    form.cleaned_data['image'] is None:
                message = 'post should contain text or an image!!'
                return render(request, 'post/create_post.html', {'message': message, 'form': form})
            else:
                validated_data = form.cleaned_data
                Post.objects.create(**validated_data, user=request.user)
                return redirect('profile', request.user.slug)
        return render(request, 'post/create_post.html')


class PostList(ListView):
    model = Post


class PostDetail(View):

    def get(self, request, slug):
        form = CommentForm()
        post_obj = Post.objects.get(slug=slug)
        return render(request, 'post/post_detail.html', {'form': form, 'object': post_obj})

    def post(self, request, slug):
        form = CommentForm(request.POST)
        delete_comment = request.POST.get('delete_comment')
        post_obj = Post.objects.get(slug=slug)

        if form.is_valid():
            if form.cleaned_data['context']:
                Comment.objects.create(user=request.user, post=post_obj, context=form.cleaned_data['context'])

        return redirect('post_detail', slug)


class DeleteComment(View):
    @staticmethod
    def get(request, pk):
        comment = Comment.objects.get(id=pk)
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', post_slug)


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/create_post.html'
    # form_class = PostUpdateForm
    form_class = PostUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def get_success_url(self):
        return reverse('post_detail', kwargs={
            'slug': self.object.slug,
        })


class DeletePost(View):

    @staticmethod
    def get(request, slug):
        post = Post.objects.get(slug=slug)
        user_slug = post.user.slug
        post.delete()
        return redirect('profile', user_slug)


class LikePost(View):
    def get(self, request, slug):
        post_obj = Post.objects.get(slug=slug)
        likes = post_obj.likes.all()
        if request.user in likes:
            post_obj.likes.remove(request.user)
        else:
            post_obj.likes.add(request.user)
        post_obj.save()
        return redirect('post_detail', slug)
