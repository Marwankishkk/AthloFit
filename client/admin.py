from django.contrib import admin

from .models import Client, Subscription

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'city', 'gender', 'age', 'height', 'weight', 'goal', 'program_name', 'program_start_date', 'program_end_date')
    list_filter = ('gender', 'goal', 'program_name')
    search_fields = ('name', 'phone_number', 'city')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'coach', 'plan_name', 'amount_paid', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('client__name', 'coach__username', 'plan_name')

admin.site.register(Client, ClientAdmin)
admin.site.register(Subscription, SubscriptionAdmin)