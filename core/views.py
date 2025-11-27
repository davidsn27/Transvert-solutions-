# -------------------------------
# IMPORTS GENERALES
# -------------------------------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login

import uuid
import json
import tempfile
import os
import qrcode
from io import BytesIO

from reportlab.lib.pagesizes import letter, A6
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from .models import Envio, SoporteTicket, SoporteRespuesta
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# -------------------------------
# LOGIN / LOGOUT / REGISTRO
# -------------------------------
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso.', extra_tags="register")
            return redirect('login')
        else:
            messages.error(request, 'Error en el registro.', extra_tags="register")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)  # <--- instancia única

    if request.method == 'POST':
        if form.is_valid():
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
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        else:
            # Agregar errores del formulario a messages
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('index')

# -------------------------------
# PANELES
# -------------------------------
@login_required(login_url='login')
def staff_panel(request):
    envios = Envio.objects.all().order_by('-id')
    tickets = SoporteTicket.objects.all().order_by('-fecha')
    return render(request, 'staff_panel.html', {'envios': envios, 'tickets': tickets})


@login_required(login_url='login')
def superadmin_panel(request):
    return render(request, 'superadmin_panel.html')


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
# CREAR ENVÍO
# -------------------------------
@login_required(login_url='login')
def crear_envio(request):
    if request.method == "POST":
        numero_guia = "G-" + uuid.uuid4().hex[:10].upper()
        try:
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
            messages.success(
                request,
                f"Envío creado correctamente. Número de guía: {numero_guia}.",
                extra_tags="envio"
            )
        except Exception as e:
            messages.error(request, f"No se pudo crear el envío: {str(e)}", extra_tags="envio")

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
            error = "No se encontró un envío con ese número de guía."

    return render(request, "seguimiento.html", {"envio": envio, "error": error})


# -------------------------------
# SOPORTE TÉCNICO
# -------------------------------
@csrf_exempt
def crear_ticket(request):
    if request.method == 'GET':
        return render(request, 'soporte.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            asunto = data.get('asunto', '').strip()
            descripcion = data.get('descripcion', '').strip()
            prioridad = data.get('prioridad', 'Media')
            correo = data.get('correo', '').strip()

            if not asunto or not descripcion or not correo:
                return JsonResponse({'mensaje': '❌ Por favor completa todos los campos'}, status=400)

            SoporteTicket.objects.create(
                usuario=request.user,
                asunto=asunto,
                descripcion=descripcion,
                prioridad=prioridad,
                correo=correo
            )

            return JsonResponse({'mensaje': '✅ Ticket enviado correctamente'})

        except Exception as e:
            return JsonResponse({'mensaje': f'❌ Error al enviar ticket: {str(e)}'}, status=500)


def ver_tickets_admin(request):
    tickets = SoporteTicket.objects.all().order_by('-fecha')
    return render(request, 'tickets.html', {'tickets': tickets})


@csrf_exempt
def responder_ticket(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)

        SoporteRespuesta.objects.create(
            ticket_id=id,
            mensaje=data.get('mensaje', ''),
            autor="ADMIN"
        )

        nuevo_estado = data.get('estado', 'EN PROCESO')
        SoporteTicket.objects.filter(id=id).update(estado=nuevo_estado)

        return JsonResponse({'success': True, 'msg': '✅ Respuesta enviada'})



# -------------------------------
# DESCARGAR ETIQUETA PDF + QR
# -------------------------------
def descargar_guia_pdf(request, envio_id):
    envio = Envio.objects.get(id=envio_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="guia_{envio.numero_guia}.pdf"'

    p = canvas.Canvas(response, pagesize=A6)

    # TEXTO
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(52*mm, 95*mm, "TRANSVERT SOLUTIONS")
    p.setFont("Helvetica", 8)
    p.drawCentredString(52*mm, 90*mm, "ETIQUETA DE ENVÍO")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(8*mm, 82*mm, f"GUÍA: {envio.numero_guia}")
    p.setFont("Helvetica", 7)
    p.drawString(8*mm, 76*mm, f"Remitente: {envio.remitente_nombre}")
    p.drawString(8*mm, 71*mm, f"Tel: {envio.remitente_telefono}")
    p.drawString(8*mm, 65*mm, f"Destinatario: {envio.destinatario_nombre}")
    p.drawString(8*mm, 60*mm, f"Tel: {envio.destinatario_telefono}")
    p.drawString(8*mm, 54*mm, f"Origen: {envio.direccion_origen}")
    p.drawString(8*mm, 49*mm, f"Destino: {envio.direccion_destino}")
    p.drawString(8*mm, 43*mm, f"Tipo: {envio.tipo_envio}")
    p.drawString(8*mm, 38*mm, f"Peso: {envio.peso} Kg")

    # QR
    qr_img = qrcode.make(envio.numero_guia)
    temp_path = os.path.join(tempfile.gettempdir(), f"{envio.numero_guia}.png")
    qr_img.save(temp_path)
    p.drawImage(temp_path, 35*mm, 10*mm, 30*mm, 30*mm)

    p.showPage()
    p.save()

    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except:
            pass

    return response


# -------------------------------
# ACTUALIZAR ESTADO ENVÍO (AJAX)
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
# CREAR ENVIO API
# -------------------------------
@csrf_exempt
def crear_envio_api(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    numero_guia = "G-" + uuid.uuid4().hex[:10].upper()

    envio = Envio.objects.create(
        numero_guia=numero_guia,
        remitente_nombre=data.get('remitente_nombre', ''),
        remitente_telefono=data.get('remitente_telefono', ''),
        remitente_email=data.get('remitente_email', ''),
        destinatario_nombre=data.get('destinatario_nombre', ''),
        destinatario_telefono=data.get('destinatario_telefono', ''),
        destinatario_email=data.get('destinatario_email', ''),
        tipo_envio=data.get('tipo_envio', ''),
        peso=data.get('peso', 0),
        dimensiones=data.get('dimensiones', ''),
        direccion_origen=data.get('direccion_origen', ''),
        direccion_destino=data.get('direccion_destino', ''),
    )

    return JsonResponse({
        'success': True,
        'msg': 'Envío creado correctamente',
        'numero_guia': envio.numero_guia
    }, status=201)
