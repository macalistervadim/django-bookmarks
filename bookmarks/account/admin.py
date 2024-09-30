from django.contrib import admin
from account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        Profile.user.field.name,
        Profile.date_of_birth.field.name,
        Profile.photo.field.name,
    ]