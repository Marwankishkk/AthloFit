from django.contrib import admin

# Register your models here.
from .models import User
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
    
admin.site.register(User, UserAdmin)
