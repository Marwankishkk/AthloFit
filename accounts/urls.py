from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path(
        'activate/<uidb64>/<token>/',
        views.activate_account,
        name='activate_account',
    ),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path(
        'reset-password/<uidb64>/<token>/',
        views.reset_password,
        name='reset_password',
    ),
    path('logout/', views.logout, name='logout'),
]