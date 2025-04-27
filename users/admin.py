from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'password')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('first_name',)
