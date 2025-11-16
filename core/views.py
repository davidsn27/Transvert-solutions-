from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Envio
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, EnvioForm
from django.http import JsonResponse
from django.conf import settings
import requests  # Para interactuar con la API de Google Maps

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. ¡Ahora puedes iniciar sesión!')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"¡Has iniciado sesión como {username}!")
                return redirect('home')
            else:
                messages.error(request, "Nombre de usuario o contraseña inválidos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña inválidos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "¡Has cerrado sesión exitosamente!")
    return redirect('index')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='staff_panel')
def staff_panel(request):
    envios = Envio.objects.all()
    estado = request.GET.get('estado')
    q = request.GET.get('q')
    if estado and estado != 'todos':
        envios = envios.filter(estado=estado)
    if q:
        envios = envios.filter(Q(numero_guia__icontains=q) | Q(cliente__icontains=q))
    paginator = Paginator(envios, 10)  # 10 envíos por página
    page_number = request.GET.get('page')
    envios = paginator.get_page(page_number)
    return render(request, 'staff_panel.html', {'envios': envios})

@login_required
def actualizar_estado_envio(request):
    if request.method == 'POST':
        envio_id = request.POST.get('envio_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        try:
            envio = Envio.objects.get(pk=envio_id)
            envio.estado = nuevo_estado
            envio.save()
            return JsonResponse({'success': True, 'nuevo_estado': nuevo_estado})
        except Envio.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Envío no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='superadmin_panel')
def superadmin_panel(request):
    return render(request, 'superadmin_panel.html')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='staff_panel')
def crear_envio(request):
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            envio = form.save()
            messages.success(request, f'Envío {envio.numero_guia} creado exitosamente.')
            return redirect('staff_panel')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = EnvioForm()
    return render(request, 'crear_envio.html', {'form': form})

def geocode_address(address):
    """
    Utiliza la API de Google Maps para obtener las coordenadas de una dirección.
    """
    params = {
        'address': address,
        'key': settings.GOOGLE_MAPS_API_KEY
    }
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None