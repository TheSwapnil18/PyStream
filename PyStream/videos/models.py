from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_videos', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_videos', blank=True)
    
    
    views = models.PositiveIntegerField(default=0)  # 👈 NEW FIELD


    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # latest comment first

    def __str__(self):
        return f"{self.user.username} on {self.video.title}"
    
class VideoView(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="views_log")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} viewed {self.video}"
