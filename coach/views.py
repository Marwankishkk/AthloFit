from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from client.forms import ClientForm
from client.models import Client


@login_required
def dashboard(request):
    stats = Client.objects.filter(coach=request.user).aggregate(
        total=Count('id'),
        active=Count('id', filter=Q(is_active=True)),
    )
    return render(
        request,
        'coach/dashboard.html',
        {
            'client_count': stats['total'] or 0,
            'active_client_count': stats['active'] or 0,
        },
    )

@login_required
def get_clients(request):
    clients = Client.objects.filter(coach=request.user).order_by('name')
    return render(request, 'coach/clients.html', {'clients': clients})

@login_required
def get_client(request, id):
    client = get_object_or_404(Client, pk=id, coach=request.user)
    return render(request, 'coach/client.html', {'client': client})

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.coach = request.user
            client.save()
            messages.success(
                request,
                f'"{client.name}" was added to your clients.',
            )
            return redirect('dashboard')
    else:
        form = ClientForm()
    return render(request, 'coach/add_client.html', {'form': form})

@login_required
def edit_client(request, id):
    client = get_object_or_404(Client, pk=id, coach=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{client.name}" was updated.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'coach/edit_client.html', {'form': form})


@login_required
def delete_client(request, id):
    client = get_object_or_404(Client, pk=id, coach=request.user)
    client.delete()
    messages.success(request, f'"{client.name}" was deleted.')
    return redirect('dashboard')