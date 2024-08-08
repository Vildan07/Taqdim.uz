from django.contrib import admin

from .models import Profile,SocialMediaIcon

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'user', 'telephone', 'location', 'about')


admin.site.register(SocialMediaIcon)