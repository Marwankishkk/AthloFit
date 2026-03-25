from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import LoginForm, PasswordResetRequestForm, UserCreationForm
from .mail import send_activation_email, send_reset_password_email
from .models import User
from .tokens import account_activation_token

def register(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
            )
            user.save()
            send_activation_email(request, user)
            messages.success(
                request,
                'We sent a link to your email. Open it to activate your account, then log in.',
            )
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can log in now.')
        return redirect('login')
    messages.error(
        request,
        'This activation link is invalid or has expired. Try registering again or contact support.',
    )
    return redirect('login')


def login(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You have been logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()
            if user is not None:
                send_reset_password_email(request, user)
            messages.success(
                request,
                'If an account exists for that email, we sent password reset instructions.',
            )
            return redirect('login')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or not default_token_generator.check_token(user, token):
        messages.error(
            request,
            'This reset link is invalid or has expired. Request a new one from the forgot password page.',
        )
        return redirect('login')
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been updated. You can log in now.')
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'accounts/reset_password.html', {'form': form})
