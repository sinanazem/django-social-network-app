from django.db import models
from django.contrib.auth.models import User 

class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150)
    body = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    
    def __str__(self) -> str:
        return self.slug + " " + user
