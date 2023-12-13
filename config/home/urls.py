from django.urls import path
from .views import HomeView, CommunityView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('community/', CommunityView.as_view(), name='community'),
]
