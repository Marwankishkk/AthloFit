from django.urls import path
from . import views

urlpatterns = [
    path('invite/', views.generate_invitation, name='generate_invitation'),
    path('invite/<uuid:token>/', views.client_form, name='client_form'),
    path('invitations/', views.pending_requests, name='pending_requests'),
    path('invitations/<int:invitation_id>/accept/', views.accept_client, name='accept_client'),
    path('invitations/<int:invitation_id>/reject/', views.reject_client, name='reject_client'),
]