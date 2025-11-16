from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Envio
from .forms import EnvioForm
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse

# 🏠 Vista principal del Home
def index(request):
    """
    Muestra la página principal (index.html)
    """
    return render(request, 'index.html')

@login_required
def home(request):
    """
    Muestra la página principal (home.html) - requiere login
    """
    return render(request, 'home.html')

# 🔐 Vista de inicio de sesión 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}! Inicio de sesión exitoso.')
            
            # 🔀 Redirección según tipo de usuario
            if user.is_superuser:
                return redirect('superadmin_panel')
            elif user.is_staff:
                return redirect('staff_panel')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Por favor, intenta de nuevo.')

    return render(request, 'login.html')

# 📝 Vista de registro
def register_view(request):
    """
    Vista para el registro de nuevos usuarios
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'register.html')
        
        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, '¡Registro completado exitosamente! Ya puedes iniciar sesión.')
        return redirect('login')  # Redirige al login después del registro
    
    return render(request, 'register.html')

def crear_envio(request):
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            envio = form.save()
            messages.success(request, f"Envío creado correctamente. Número de guía: {envio.numero_guia}")
            return redirect('crear_envio')
    else:
        form = EnvioForm()
    return render(request, 'crear_envio.html', {'form': form})


def seguimiento_view(request):
    resultado = None
    if request.method == 'POST':
        numero_guia = request.POST.get('guia')
        envio = Envio.objects.filter(numero_guia=numero_guia).first()

        if envio:
            resultado = {
                'numero_guia': envio.numero_guia,
                'descripcion': envio.descripcion,
                'estado': envio.estado,
                'fecha_envio': envio.fecha_envio.strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            resultado = {
                'numero_guia': numero_guia,
                'descripcion': 'No encontrado',
                'estado': '-',
                'fecha_envio': '-'
            }

    return render(request, 'seguimiento.html', {'resultado': resultado})

# 🚪 Vista de cerrar sesión
def logout_view(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('index')

# ℹ️ Vista de contacto
def about_view(request):
    """
    Vista de información o 'Acerca de'
    """
    return render(request, 'contact.html')

@staff_member_required

# Panel principal
def staff_panel(request):
    hoy = timezone.now().date()
    inicio = timezone.make_aware(timezone.datetime.combine(hoy, timezone.datetime.min.time()))
    fin = timezone.make_aware(timezone.datetime.combine(hoy, timezone.datetime.max.time()))

    total_usuarios = User.objects.count()
    total_envios = Envio.objects.count()
    pedidos_hoy = Envio.objects.filter(fecha_envio__range=(inicio, fin)).count()
    envios = Envio.objects.all().order_by('-fecha_envio')

    return render(request, 'staff_panel.html', {
        'total_usuarios': total_usuarios,
        'total_envios': total_envios,
        'pedidos_hoy': pedidos_hoy,
        'envios': envios
    })

# Vista para actualizar estado vía AJAX
def actualizar_estado_envio(request):
    if request.method == 'POST':
        envio_id = request.POST.get('envio_id')
        nuevo_estado = request.POST.get('nuevo_estado')
        envio = get_object_or_404(Envio, id=envio_id)
        envio.estado = nuevo_estado
        envio.save()
        return JsonResponse({'success': True, 'nuevo_estado': nuevo_estado})
    return JsonResponse({'success': False})

# 🧑‍💼 Panel de Super Administrador
from django.contrib.auth.decorators import login_required

@login_required
def superadmin_panel(request):
    """
    Vista para el panel del superadministrador
    """
    if not request.user.is_superuser:
        # Si el usuario no es superadmin, lo redirige al home
        return redirect('home')
    return render(request, 'superadmin_panel.html')