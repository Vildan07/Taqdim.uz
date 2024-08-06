from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    sites = models.JSONField(blank=True, null=True)
    location = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super().save(*args, **kwargs)