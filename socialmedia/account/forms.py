from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    cofirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("Your Username Already Exist")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("Your Email Already Exist")

        return email
    
    def clean(self):
        cd = super().clean()
        password = cd.get("password")
        cofirm_password = cd.get("cofirm_password")
        if password and cofirm_password and password != cofirm_password:
            raise ValidationError("Password not Match")

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ("age", "bio")

