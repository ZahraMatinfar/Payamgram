from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from apps.post.forms import PostForm, CommentForm
from apps.post.models import Post, Comment


class CreatePost(LoginRequiredMixin, View):
    """
    view of creating post
    """

    def get(self, request):
        form = PostForm()
        return render(request, 'post/create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            post = Post(**validated_data, user=request.user)
            post.save()
            return redirect('profile', request.user.slug)
        return render(request, 'post/create_post.html', {'form': form})


class PostList(ListView):
    model = Post


# class PostDetail(DetailView):
#     model = Post


# class CommentView(CreateView):
#     model = Comment
#     template_name = 'post/post_detail.html'
#     form_class = CommentForm
#     # success_url = '/thanks/'
#     def form_valid(self, form):
#         comment = Comment.objects.create(u)


class PostDetail(View):

    def get(self, request, slug):
        form = CommentForm()
        post_obj = Post.objects.get(slug=slug)
        return render(request, 'post/post_detail.html', {'form': form, 'object': post_obj})

    def post(self, request, slug):
        form = CommentForm(request.POST)
        like = request.POST.get('like')
        delete = request.POST.get('delete')
        post_obj = Post.objects.get(slug=slug)
        if delete is not None:
            post_obj.delete()
            return redirect('profile', request.user.slug)
        if form.is_valid():
            if form.cleaned_data['context']:
                comment = Comment.objects.create(user=request.user, post=post_obj, context=form.cleaned_data['context'])
                comment.save()
        if like is not None:
            likes = post_obj.likes.all()
            if request.user in likes:
                post_obj.likes.remove(request.user)
            else:
                post_obj.likes.add(request.user)
            post_obj.save()

            return redirect('post_detail', slug)
        return render(request, 'post/post_detail.html', {'form': form, 'object': post_obj})
