from django import forms

from apps.post.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'caption']
        labels = {
            'title': 'عنوان',
            'caption': 'متن',
        }
