from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/', views.get_clients, name='client_list'),
    path('client/<int:id>/', views.get_client, name='client_detail'),
    path('clients/edit/<int:id>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:id>/', views.delete_client, name='delete_client'),
]
