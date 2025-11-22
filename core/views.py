from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import uuid
import json

from .models import Envio
from .forms import CustomUserCreationForm, CustomAuthenticationForm


# -------------------------------
#  LOGOUT
# -------------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('index')


# -------------------------------
#  CREAR ENVÍO (FORMULARIO)
# -------------------------------
def crear_envio(request):
    if request.method == "POST":
        numero_guia = "G-" + uuid.uuid4().hex[:10].upper()

        Envio.objects.create(
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
            direccion_origen=request.POST.get("direccion_origen"),
            direccion_destino=request.POST.get("direccion_destino"),
        )

        messages.success(request, f"Envío creado correctamente. Número de guía: {numero_guia}")
        return redirect("crear_envio")

    return render(request, "crear_envio.html")


# -------------------------------
#  API CREAR ENVÍO
# -------------------------------
@csrf_exempt
def crear_envio_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    numero_guia = data.get('numero_guia', "G-" + uuid.uuid4().hex[:10].upper())

    envio = Envio.objects.create(
        numero_guia=numero_guia,
        cliente=data.get('cliente', ''),
        descripcion=data.get('descripcion', ''),
        estado=data.get('estado', 'pendiente'),
        direccion_origen=data.get('direccion_origen', ''),
        direccion_destino=data.get('direccion_destino', ''),
    )

    return JsonResponse({
        'success': True,
        'msg': f'Envío {envio.numero_guia} creado.',
        'envio_id': envio.pk
    }, status=201)


# -------------------------------
#  PÁGINAS PÚBLICAS
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
#  REGISTRO
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# -------------------------------
#  LOGIN
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)

                # 🔥 CORREGIDO: ahora usa el grupo correcto
                if user.groups.filter(name='admin').exists():
                    return redirect('staff_panel')

                return redirect('home')

        messages.error(request, "Credenciales inválidas.")

    return render(request, 'login.html', {'form': CustomAuthenticationForm()})


# -------------------------------
#  PANEL STAFF (admin)
# -------------------------------
@login_required(login_url='login')
@user_passes_test(lambda u: u.groups.filter(name='admin').exists(), login_url='home')
def staff_panel(request):
    envios = Envio.objects.all().order_by('-id')

    estado = request.GET.get('estado')
    q = request.GET.get('q')

    # FILTRO POR ESTADO
    if estado and estado != 'todos':
        envios = envios.filter(estado=estado)

    # FILTRO DE BÚSQUEDA CORREGIDO
    if q:
        envios = envios.filter(
            Q(numero_guia__icontains=q) |
            Q(remitente_nombre__icontains=q) |
            Q(remitente_email__icontains=q) |
            Q(remitente_telefono__icontains=q) |
            Q(destinatario_nombre__icontains=q) |
            Q(destinatario_email__icontains=q) |
            Q(destinatario_telefono__icontains=q)
        )

    return render(request, 'staff_panel.html', {'envios': envios})


# -------------------------------
#  ACTUALIZAR ESTADO
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
#  SUPERADMIN PANEL
# -------------------------------
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def superadmin_panel(request):
    return render(request, 'superadmin_panel.html')


# -------------------------------
#  SEGUIMIENTO DE ENVÍO
# -------------------------------
def seguimiento_envio(request):
    envio = None
    error = None

    if 'numero_guia' in request.GET:
        try:
            envio = Envio.objects.get(numero_guia=request.GET.get('numero_guia'))
        except Envio.DoesNotExist:
            error = "No se encontró un envío con ese número de guía."

    return render(request, "seguimiento.html", {"envio": envio, "error": error})
