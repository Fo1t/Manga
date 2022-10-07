from django.contrib import admin
from .models import UserSettings
# Register your models here.


@admin.register(UserSettings)
class ImageAdmin(admin.ModelAdmin):
    model = UserSettings
    list_display = ('id', 'user', 'mode')