from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    a form for creating post
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = ['title', 'caption', 'image']


class CommentForm(forms.ModelForm):
    """
    a form for creating post
    """

    class Meta:
        model = Comment
        fields = ['context']
        widgets = {
            'context': forms.TextInput(attrs={'placeholder': 'Leave a comment'})
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'caption', 'image')
