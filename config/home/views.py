from django.shortcuts import render
from django.views import View
# Create your views here.
# def home(requests):
#     return render(requests, 'home/index.html')

class HomeView(View):
    def get(self, requests):
        return render(requests, 'home/index.html')
    
    def post(self, requests):
        pass