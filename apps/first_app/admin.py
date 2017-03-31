from django.contrib import admin
from .models import User, Friend

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email']

admin.site.register(User, UserAdmin)
# Register your models here.
