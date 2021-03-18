from django import forms

from apps.post.models import Post, Comment


class PostForm(forms.ModelForm):
    """
    a form for creating post
    """

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

    def save(self, user=None):
        post = super().save(commit=False)
        if user:
            post.user = user
        post.save()
        return post
