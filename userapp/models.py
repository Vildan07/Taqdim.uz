from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

    # def save(self, *args, **kwargs):
    #     if not self.username:
    #         self.username = slugify(self.user.username)
    #     super().save(*args, **kwargs)
