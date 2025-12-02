# -------------------------------
# IMPORTS GENERALES
# -------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings # NUEVO: Importamos settings

import uuid
import json
import tempfile
import os
import qrcode
# NUEVO: Importamos el cliente de Gemini
from google import genai 

from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas

from .models import Envio, SoporteTicket, SoporteRespuesta
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# -------------------------------
# LOGIN / LOGOUT / REGISTRO
# -------------------------------
def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Registro exitoso.')
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('superadmin_panel')
            elif user.is_staff:
                return redirect('staff_panel')
            else:
                return redirect('home')
        messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')

# -------------------------------
# PÁGINAS PÚBLICAS
# -------------------------------
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')

# -------------------------------
# PANELES
# -------------------------------
@login_required(login_url='login')
def staff_panel(request):
    envios = Envio.objects.all().order_by('-id')
    tickets = SoporteTicket.objects.all().order_by('-fecha')

    # Filtrar envíos
    estado_envio = request.GET.get('estado_envio')
    if estado_envio:
        envios = envios.filter(estado=estado_envio)

    # Filtrar tickets
    estado_ticket = request.GET.get('estado_ticket')
    if estado_ticket:
        tickets = tickets.filter(estado=estado_ticket)

    return render(request, 'staff_panel.html', {
        'envios': envios,
        'tickets': tickets
    })


@login_required(login_url='login')
def superadmin_panel(request):
    usuarios = User.objects.all()
    envios = Envio.objects.all().order_by('-fecha_creado')
    tickets = SoporteTicket.objects.all().order_by('-fecha')

    # Filtrar envíos
    estado_envio = request.GET.get('estado_envio')
    if estado_envio:
        envios = envios.filter(estado=estado_envio)

    # Filtrar tickets
    estado_ticket = request.GET.get('estado_ticket')
    if estado_ticket:
        tickets = tickets.filter(estado=estado_ticket)

    return render(request, 'superadmin_panel.html', {
        'usuarios': usuarios,
        'envios': envios,
        'tickets': tickets
    })

# -------------------------------
# CREAR ENVÍO
# -------------------------------
@login_required(login_url='login')
def crear_envio(request):
    if request.method == 'POST':
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
            peso=request.POST.get("peso") or 0,
            dimensiones=request.POST.get("dimensiones") or "",
            direccion_origen=request.POST.get("direccion_origen"),
            direccion_destino=request.POST.get("direccion_destino"),
        )
        messages.success(request, f"Envío creado: {numero_guia}")
        return redirect("crear_envio")
    return render(request, "crear_envio.html")

# -------------------------------
# SEGUIMIENTO
# -------------------------------
def seguimiento_envio(request):
    envio = None
    error = None
    if 'numero_guia' in request.GET:
        try:
            envio = Envio.objects.get(numero_guia=request.GET.get('numero_guia'))
        except Envio.DoesNotExist:
            error = "No se encontró un envío."
    return render(request, "seguimiento.html", {"envio": envio, "error": error})

# -------------------------------
# SOPORTE
# -------------------------------
@csrf_exempt
def crear_ticket(request):
    if request.method == 'GET':
        return render(request, 'soporte.html')

    data = json.loads(request.body.decode('utf-8')) if request.body else {}
    SoporteTicket.objects.create(
        usuario=request.user,
        asunto=data.get('asunto'),
        descripcion=data.get('descripcion'),
        correo=data.get('correo')
    )
    return JsonResponse({'success': True})


@login_required
def ver_tickets_admin(request):
    tickets = SoporteTicket.objects.all().order_by('-fecha')
    return render(request, 'tickets.html', {'tickets': tickets})

# -------------------------------
# RESPONDER TICKET Y CAMBIAR ESTADO
# -------------------------------
@login_required
@csrf_exempt
def responder_ticket(request, id):
    if request.method == 'POST':
        ticket = get_object_or_404(SoporteTicket, id=id)
        mensaje = request.POST.get("mensaje")
        estado = request.POST.get("estado")

        if mensaje:
            SoporteRespuesta.objects.create(
                ticket=ticket,
                usuario=request.user,
                mensaje=mensaje
            )

        if estado:
            ticket.estado = estado
            ticket.save()

        messages.success(request, f"Ticket {ticket.id} actualizado correctamente.")
    return redirect('staff_panel')

# -------------------------------
# ACTUALIZAR ESTADO ENVÍO
# -------------------------------
@login_required
def actualizar_estado_envio(request):
    if request.method == 'POST':
        envio_id = request.POST.get("envio_id")
        nuevo_estado = request.POST.get("nuevo_estado")
        envio = get_object_or_404(Envio, id=envio_id)
        envio.estado = nuevo_estado
        envio.save()
        messages.success(request, f"Estado de {envio.numero_guia} actualizado a {nuevo_estado}")
    return redirect('staff_panel')

# -------------------------------
# PDF + QR
# -------------------------------
def descargar_guia_pdf(request, envio_id):
    envio = get_object_or_404(Envio, id=envio_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=guia_{envio.numero_guia}.pdf'
    p = canvas.Canvas(response, pagesize=A6)
    p.drawString(20, 750, "TRANSVERT SOLUTIONS")
    p.drawString(20, 730, f"GUIA: {envio.numero_guia}")
    p.drawString(20, 710, f"ORIGEN: {envio.direccion_origen}")
    p.drawString(20, 690, f"DESTINO: {envio.direccion_destino}")

    qr = qrcode.make(envio.numero_guia)
    path = os.path.join(tempfile.gettempdir(), "qr.png")
    qr.save(path)
    p.drawImage(path, 150, 650, 100, 100)

    p.showPage()
    p.save()
    return response

# -------------------------------
# API CREAR ENVÍO
# -------------------------------
@csrf_exempt
def crear_envio_api(request):
    data = json.loads(request.body.decode('utf-8'))
    numero_guia = "G-" + uuid.uuid4().hex[:10].upper()
    envio = Envio.objects.create(
        numero_guia=numero_guia,
        remitente_nombre=data.get('remitente_nombre'),
        remitente_telefono=data.get('remitente_telefono'),
        remitente_email=data.get('remitente_email'),
        destinatario_nombre=data.get('destinatario_nombre'),
        destinatario_telefono=data.get('destinatario_telefono'),
        destinatario_email=data.get('destinatario_email'),
        tipo_envio=data.get('tipo_envio'),
        peso=data.get('peso', 0),
        dimensiones=data.get('dimensiones', ''),
        direccion_origen=data.get('direccion_origen'),
        direccion_destino=data.get('direccion_destino'),
    )
    return JsonResponse({'success': True, 'numero_guia': envio.numero_guia})


# -------------------------------
# CHATBOT GEMINI (NUEVA FUNCIÓN)
# -------------------------------
@csrf_exempt
def chatbot_response(request):
    """
    Maneja la solicitud del usuario, llama a la API de Gemini y devuelve la respuesta.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Solo se acepta POST.'}, status=405)

    try:
        # 1. Obtener el prompt/pregunta del usuario
        data = json.loads(request.body.decode('utf-8'))
        prompt = data.get('prompt')

        if not prompt:
            return JsonResponse({'error': 'Pregunta no proporcionada en el cuerpo de la solicitud (prompt).'}, status=400)

        # 2. Configurar el cliente de Gemini
        # La clave es cargada desde settings.py
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # 3. Llamar a la API de Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # 4. Devolver la respuesta en formato JSON
        return JsonResponse({
            'success': True,
            'response': response.text
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Formato JSON inválido en el cuerpo de la solicitud.'}, status=400)
    except Exception as e:
        # Manejar errores de la API, red, etc.
        error_message = f'Error interno del chatbot. Asegúrate que la clave API es correcta y que tienes conexión. Detalle: {str(e)}'
        print(f"Error de Gemini API: {e}")
        return JsonResponse({'success': False, 'error': error_message}, status=500)
        
