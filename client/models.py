from django.conf import settings
from django.db import models
from django.utils import timezone

from .validators import validate_phone_number

class Client(models.Model):
    # Link each client to a specific coach
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='clients'
    )
    
    # Basic Info
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        help_text='8–15 digits. You can include spaces, +, or dashes (e.g. 01xxxxxxxxx or +20 1xx …).',
    ) 
    city = models.CharField(max_length=100, blank=True)
    
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Vital Stats
    age = models.PositiveIntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    
    # Program Details
    GOAL_CHOICES = [
        ('CUT', 'Fat Loss'),
        ('BULK', 'Muscle Gain'),
        ('MAINTAIN', 'Maintenance'),
        ('ATHLETIC', 'Athletic Performance'),
    ]
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    
    program_name = models.CharField(max_length=255) 
    is_active = models.BooleanField(default=True)
    
    program_start_date = models.DateField() 
    program_end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ({self.coach.username}'s Client)"


class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    plan_name = models.CharField(max_length=100) # e.g., "3-Month Transformation"
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now().date() > self.end_date