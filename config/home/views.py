from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import PostModel
# Create your views here.
# def home(requests):
#     return render(requests, 'home/index.html')

class HomeView(View):
    def get(self, requests):
        posts = PostModel.objects.all()
        return render(requests, 'home/index.html', {'posts':posts})
    
class CommunityView(View):
    def get(self, requests):
        users = User.objects.all()
        return render(requests, 'home/community.html',{"users":users})
 