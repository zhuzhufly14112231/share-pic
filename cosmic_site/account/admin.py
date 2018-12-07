from django.contrib import admin
from account.models import Profile, Content
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'photo')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('user_form', 'user_to', 'created')

