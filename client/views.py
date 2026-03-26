from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import ClientInvitation, Client
from .forms import ClientInvitationForm


@login_required
def generate_invitation(request):
    invitation = ClientInvitation.objects.create(coach=request.user)
    link = request.build_absolute_uri(f'/invite/{invitation.token}/')
    return render(request, 'invitations/generated.html', {
        'link': link,
        'invitation': invitation,
    })


def client_form(request, token):
    invitation = get_object_or_404(ClientInvitation, token=token)

    if invitation.status != 'pending':
        return render(request, 'invitations/already_used.html')

    if request.method == 'POST':
        form = ClientInvitationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            invitation.name = d['name']
            invitation.phone_number = d['phone_number']
            invitation.city = d['city']
            invitation.gender = d['gender']
            invitation.age = d['age']
            invitation.height = d['height']
            invitation.weight = d['weight']
            invitation.goal = d['goal']
            invitation.status = 'submitted'
            invitation.submitted_at = timezone.now()
            invitation.save()
            return render(request, 'invitations/thank_you.html', {
                'coach': invitation.coach
            })
    else:
        form = ClientInvitationForm()

    return render(request, 'invitations/client_form.html', {
        'form': form,
        'coach': invitation.coach,
    })


@login_required
def pending_requests(request):
    invitations = ClientInvitation.objects.filter(
        coach=request.user,
        status='submitted'
    ).order_by('-submitted_at')
    return render(request, 'invitations/pending.html', {'invitations': invitations})


@login_required
def accept_client(request, invitation_id):
    invitation = get_object_or_404(ClientInvitation, id=invitation_id, coach=request.user)

    if invitation.status != 'submitted':
        messages.error(request, 'This request is no longer valid.')
        return redirect('pending_requests')

    Client.objects.create(
        coach=request.user,
        name=invitation.name,
        phone_number=invitation.phone_number,
        city=invitation.city,
        gender=invitation.gender,
        age=invitation.age,
        height=invitation.height,
        weight=invitation.weight,
        goal=invitation.goal,
        program_name='TBD',                          
        program_start_date=timezone.now().date(),
        program_end_date=timezone.now().date(),
    )

    invitation.status = 'accepted'
    invitation.save()

    messages.success(request, f'{invitation.name} has been added to your clients!')
    return redirect('pending_requests')


@login_required
def reject_client(request, invitation_id):
    invitation = get_object_or_404(ClientInvitation, id=invitation_id, coach=request.user)
    invitation.status = 'rejected'
    invitation.save()
    messages.info(request, f'Request from {invitation.name} has been rejected.')
    return redirect('pending_requests')