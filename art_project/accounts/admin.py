from django.contrib import admin
from art_project.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'first_name', 'last_name')
