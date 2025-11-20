from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Envio
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EnvioForm
from django.http import JsonResponse
from django.conf import settings
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import random
import uuid


# -------------------------------
# FORMULARIO PARA CREAR ENVÍO
# -------------------------------
def crear_envio(request):
    if request.method == "POST":
        # Generar número de guía único
        numero_guia = "G-" + uuid.uuid4().hex[:10].upper()

        envio = Envio.objects.create(
            numero_guia=numero_guia,
            remitente_nombre=request.POST.get("remitente_nombre"),
            remitente_telefono=request.POST.get("remitente_telefono"),
            remitente_email=request.POST.get("remitente_email"),
            destinatario_nombre=request.POST.get("destinatario_nombre"),
            destinatario_telefono=request.POST.get("destinatario_telefono"),
            destinatario_email=request.POST.get("destinatario_email"),
            tipo_envio=request.POST.get("tipo_envio"),
            peso=request.POST.get("peso"),
            dimensiones=request.POST.get("dimensiones"),
            origen=request.POST.get("direccion_origen"),
            direccion_origen=request.POST.get("direccion_origen"),
            destino=request.POST.get("direccion_destino"),
            direccion_destino=request.POST.get("direccion_destino"),
        )

        messages.success(request, f"Envío creado correctamente. Número de guía: {numero_guia}")
        return redirect("crear_envio")  # vuelve al formulario

    # Si no es POST, solo renderiza el formulario
    return render(request, "crear_envio.html")


# -------------------------------
# API PARA CREAR ENVÍO
# -------------------------------
@csrf_exempt
def crear_envio_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        payload = {}

    data = payload or request.POST

    numero_guia = data.get('numero_guia', "G-" + uuid.uuid4().hex[:10].upper())
    cliente = data.get('cliente')
    descripcion = data.get('descripcion', '')
    estado = data.get('estado', 'pendiente')
    direccion_origen = data.get('direccion_origen', '')
    direccion_destino = data.get('direccion_destino', '')

    if not cliente:
        return JsonResponse({'success': False, 'error': 'Faltan datos obligatorios'}, status=400)

    try:
        envio = Envio.objects.create(
            numero_guia=numero_guia,
            cliente=cliente,
            descripcion=descripcion,
            estado=estado,
            direccion_origen=direccion_origen,
            direccion_destino=direccion_destino
        )
        return JsonResponse({
            'success': True,
            'msg': f'Envío {envio.numero_guia} creado.',
            'envio_id': envio.pk
        }, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



# -------------------------------
#   PÁGINAS PÚBLICAS
# -------------------------------

def home(request):
    return render(request, 'home.html')

def seguimiento(request):
    return render(request, 'seguimiento.html')

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')


# -------------------------------
#   AUTENTICACIÓN
# -------------------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': CustomUserCreationForm()})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.error(request, "Credenciales inválidas.")
        else:
            messages.error(request, "Credenciales inválidas.")
    return render(request, 'login.html', {'form': CustomAuthenticationForm()})


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('index')


# -------------------------------
#    STAFF PANEL
# -------------------------------

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff, login_url='home')   # 👉 OPCIÓN B
def staff_panel(request):
    envios = Envio.objects.all()

    estado = request.GET.get('estado')
    q = request.GET.get('q')

    if estado and estado != 'todos':
        envios = envios.filter(estado=estado)
    if q:
        envios = envios.filter(Q(numero_guia__icontains=q) | Q(cliente__icontains=q))

    paginator = Paginator(envios, 10)
    page_number = request.GET.get('page')
    envios = paginator.get_page(page_number)

    return render(request, 'staff_panel.html', {'envios': envios})


# -------------------------------
#   ACTUALIZAR ESTADO
# -------------------------------

@login_required(login_url='login')
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


# -------------------------------
#   SUPERADMIN PANEL
# -------------------------------

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')   # 👉 También corregido
def superadmin_panel(request):
    return render(request, 'superadmin_panel.html')



# -------------------------------
#   GEOLOCALIZACIÓN (opcional)
# -------------------------------

def geocode_address(address):
    params = {'address': address, 'key': settings.GOOGLE_MAPS_API_KEY}
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        loc = data['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    return None, None

def seguimiento_envio(request):
    envio = None
    error = None

    if 'numero_guia' in request.GET:  # solo se procesa al dar "Consultar"
        numero_guia = request.GET.get('numero_guia')
        if numero_guia:
            try:
                envio = Envio.objects.get(numero_guia=numero_guia)
            except Envio.DoesNotExist:
                error = "No se encontró un envío con ese número de guía."

    return render(request, "seguimiento.html", {"envio": envio, "error": error})

