from django import forms

from apps.post.models import Post


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
