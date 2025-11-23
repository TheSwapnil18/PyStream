from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    # You can add more fields later like:
    # profile_image = models.ImageField(upload_to="profiles/", default="default.png")
    # subscribers = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username still required but login will be with email

    def __str__(self):
        return self.email
