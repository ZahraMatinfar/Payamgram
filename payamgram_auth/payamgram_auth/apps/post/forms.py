from django import forms

from apps.post.models import Post, Comment


class PostForm(forms.ModelForm):
    """
    a form for creating post
    """
    class Meta:
        model = Post
        fields = ['title', 'caption']
        labels = {
            'title': 'عنوان',
            'caption': 'متن',
        }


class CommentForm(forms.ModelForm):
    """
    a form for creating post
    """
    class Meta:
        model = Comment
        fields = ['context']
        # labels = {
        #     'title': 'عنوان',
        #     'caption': 'متن',
        # }
