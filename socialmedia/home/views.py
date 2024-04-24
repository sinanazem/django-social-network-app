from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm, CommentCreateForm, ReplyAddForm, SearchPostForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    form = SearchPostForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = posts.filter(content__contains=request.GET["search"])
        return render(request, "home/home.html", {"posts": posts, "form": self.form})
    

class PostDetailView(View):
    form = CommentCreateForm
    reply_form = ReplyAddForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance = Post.objects.get(pk=kwargs["post_id"], slug=kwargs["post_slug"])
        return super().setup(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        # user = User.objects.get(pk=post)
        comments = self.post_instance.pcomment.filter(is_reply=False)
        user_can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            user_can_like = True
        return render(request, "home/post_detail.html", {"post": self.post_instance, "comments": comments, "form": self.form, "reply_form": self.reply_form, "user_can_like": user_can_like})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "Your Comment Submitted successfull", extra_tags="success")
            return redirect("home:post_detail", self.post_instance.id, self.post_instance.slug)

        
    
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post_delete = get_object_or_404(Post, pk=post_id)
        if post_delete.user.id == request.user.id:
            post_delete.delete()
            messages.success(request, "Your Post Deleted Successfully", extra_tags="success")
        else:
            messages.error(request, "Your Post Wasn't Deleted", extra_tags="danger")
    
        return redirect("home:home")
    

class PostUpdateView(LoginRequiredMixin, View):
    form = PostCreateUpdateForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance = Post.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_update = self.post_instance
        if not request.user.id == post_update.user.id:
            messages.error(request, "You Cant Update This Post")
            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form(instance=post)
        return render(request, "home/update.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["content"][:30])
            new_post.save()
            messages.success(request, "Your Post Updated")
            return redirect("home:post_detail", post.id, post.slug)

class PostCreateView(LoginRequiredMixin, View):
    form = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form
        return render(request, "home/post_create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["content"][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "You Create a New Post", extra_tags="success")
            return redirect("home:post_detail", new_post.id, new_post.slug)
        

class ReplyAddView(LoginRequiredMixin, View):
    

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = ReplyAddForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "Your Reply Submitted Successfully", extra_tags="success")

        return redirect("home:post_detail",  post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, "You Hve Already This Post", extra_tags="danger")
        else:
            Vote.objects.create(user=request.user, post=post)
            messages.success(request, "You Liked This Post")

        return redirect("home:post_detail", post.id, post.slug)


