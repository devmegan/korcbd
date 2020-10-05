from django import forms
from .models import Post, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'tag_1', 'tag_2', 'tag_3')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a Title Here'
            }),
            'author': forms.HiddenInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'id': 'author_id'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post here'
            }),
            'tag_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ie: "Judo"'
            }),
            'tag_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ie: "KORCBD"'
            }),
            'tag_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ie: "Physio"'
            })
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'comment_body')

        widgets = {
            'author': forms.HiddenInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'id': 'author_id'
            }),
            'comment_body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here'
            }),
        }