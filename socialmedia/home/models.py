from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated", "-date_posted")

    def __str__(self) -> str:
        return f"{self.title} - {self.user}"
    
    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id, self.slug))
    
    def like_count(self):
        return  self.pvote.count()
    
    def user_can_like(self, user):
         user_like = user.uvote.filter(post=self)
         if user_like.exists():
             return True
         return False
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomment")
    reply = models.ForeignKey("self", on_delete=models.CASCADE, related_name="rcomment", blank=True, null=True)
    body = models.TextField()
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.body[:30]}"
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvote")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pvote")

    def __str__(self) -> str:
        return f"{self.user} - {self.post}"