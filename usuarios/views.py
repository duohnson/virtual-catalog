from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile


def registro_view(request):
    """Registra un nuevo usuario y lo autentica automáticamente."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    """Autentica al usuario con sus credenciales."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    """Cierra la sesión activa y redirige al inicio."""
    logout(request)
    messages.info(request, 'Has cerrado sesión.')
    return redirect('index')


@login_required
def perfil_view(request):
    """Muestra y permite actualizar la foto de perfil del usuario."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'foto_perfil' in request.FILES:
            profile.foto_perfil = request.FILES['foto_perfil']
            profile.save()
            messages.success(request, 'Foto de perfil actualizada.')
        return redirect('perfil')

    return render(request, 'usuarios/perfil.html', {'profile': profile})
