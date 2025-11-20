from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Envio

# ==============================
# FORMULARIO DE REGISTRO
# ==============================
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# ==============================
# LOGIN PERSONALIZADO
# ==============================
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


# ==============================
# FORMULARIO DE ENVÍOS
# ==============================
class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = [
            'numero_guia',
            'remitente_nombre',
            'remitente_telefono',
            'remitente_email',
            'destinatario_nombre',
            'destinatario_telefono',
            'destinatario_email',
            'tipo_envio',
            'peso',
            'dimensiones',
            'origen',
            'direccion_origen',
            'destino',
            'direccion_destino',
        ]
