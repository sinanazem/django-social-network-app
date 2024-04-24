from django import forms
from .models import Post, Comment

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content",)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class":"form-control"})
        }

class ReplyAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class  SearchPostForm(forms.Form):
    search = forms.CharField(max_length=200)
