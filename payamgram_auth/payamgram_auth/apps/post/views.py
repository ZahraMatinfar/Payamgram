from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView, DeleteView
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
        delete_comment = request.POST.get('delete_comment')
        post_obj = Post.objects.get(slug=slug)
        if delete is not None:
            post_obj.delete()
            return redirect('profile', request.user.slug)
        # if delete_comment is not None:
        #     comment = Comment.objects.get(user=request.user)
        #     comment.delete()
        #     return redirect('profile', request.user.slug)
        if form.is_valid():
            if form.cleaned_data['context']:
                comment = Comment.objects.create(user=request.user, post=post_obj, context=form.cleaned_data['context'])
                comment.save()
                # return redirect('post_detail', slug)
        if like is not None:
            likes = post_obj.likes.all()
            if request.user in likes:
                post_obj.likes.remove(request.user)
            else:
                post_obj.likes.add(request.user)
            post_obj.save()

        return redirect('post_detail', slug)
        # return render(request, 'post/post_detail.html', {'form': form, 'object': post_obj})


# class DeleteComment(DeleteView):
#     model = Comment
#
#     def delete(self, request, *args, **kwargs):
#         """
#         Call the delete() method on the fetched object and then redirect to the
#         success URL.
#         """
#         self.object = self.get_object()
#         post_slug = self.object.post.slug
#         self.object.delete()
#         return redirect('post_detail', post_slug)
class DeleteComment(View):
    def get(self, request, pk):
        comment = Comment.objects.get(id=pk)
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', post_slug)
        # return redirect('index')
