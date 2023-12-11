from django.shortcuts import render
from django.views import View
from .forms import UserRegistrationForm

class RegisterView(View):
    def get(self, requests):
        form = UserRegistrationForm()
        return render(requests, 'account/register.html',{"form":form})
    def post(self, requests):
        return render(requests, 'account/register.html')
