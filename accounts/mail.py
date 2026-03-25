from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def send_activation_email(request, user):
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    path = reverse(
        'activate_account',
        kwargs={'uidb64': uid, 'token': token},
    )
    activate_url = request.build_absolute_uri(path)
    context = {'user': user, 'activate_url': activate_url}
    subject = render_to_string('emails/activate_account_subject.txt', context).strip()
    body_text = render_to_string('emails/activate_account.txt', context)
    body_html = render_to_string('emails/activate_account.html', context)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(body_html, 'text/html')
    msg.send()


def send_reset_password_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    path = reverse(
        'reset_password',
        kwargs={'uidb64': uid, 'token': token},
    )
    reset_url = request.build_absolute_uri(path)
    context = {'user': user, 'reset_url': reset_url}
    subject = render_to_string('emails/reset_password_subject.txt', context).strip()
    body_text = render_to_string('emails/reset_password.txt', context)
    body_html = render_to_string('emails/reset_password.html', context)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(body_html, 'text/html')
    msg.send()
