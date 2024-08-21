from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# Create your models here.

def validate_pdf_size(value):
    limit = 20 * 1024 * 1024  # 20 МБ в байтах
    if value.size > limit:
        raise ValidationError(f'Fayl juda katta. Maksimal fayl hajmi 20 MB.')


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    sites = models.JSONField(blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(blank=True)
    pdf = models.FileField(
        upload_to='pdfs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf']), validate_pdf_size]  # Добавьте валидатор
    )
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super().save(*args, **kwargs)


class SocialMediaIcon(models.Model):
    url_pattern = models.CharField(max_length=255, unique=True)
    svg = models.FileField(upload_to='svgs/', blank=True, null=True)

    def __str__(self):
        return self.url_pattern