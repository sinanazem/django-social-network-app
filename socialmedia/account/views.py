from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation, Profile
# Create your views here.


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "account/register.html"


    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password"])
            messages.success(request, "You are Registered Successfully", extra_tags="success")

            return redirect("home:home")
        
        return render(request, self.template_name, {"form":form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)
    

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "You Logged Successfully", extra_tags="success")
                if self.next:
                    return redirect(self.next)

                return redirect("home:home")
    
            messages.error(request, "Username or Password is Wrong", extra_tags="warning")

        return render(request, self.template_name, {"form":form})
    

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You Logged Out Successfully", extra_tags="success")
        return redirect("home:home")
    

class UserProfileView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        posts = user.posts.all()
        profile = Profile.objects.get(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True

        return render(request, "account/profile.html", {"user": user, "posts": posts, "is_following": is_following, "profile": profile})

class CommunityView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all() 
        return render(request, "account/community.html", {"users": users})
    
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.success(request, "You Already Following This User", extra_tags="danger")
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, "You Followed This User", extra_tags="success")

        return redirect("account:user_profile", user.id)



class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, "You Unfollow this User", extra_tags="success")
        else:
            messages.success(request, "You Not Follow This User")

        return redirect("account:user_profile", user.id)


class EditProfileView(LoginRequiredMixin, View):
    form_class = UserEditForm

    def get(self, request):
        edit_profile = self.form_class(instance=request.user.profile, initial={"email": request.user.email})
        return render(request, "account/edit_profile.html", {"edit_profile": edit_profile})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "You Edited Profile Successfully", extra_tags="success")

        return redirect("account:user_profile", request.user.id)
