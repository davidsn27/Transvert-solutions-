from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class CustomAuthenticationForm(AuthenticationForm):
    pass  # Usa el formulario de autenticación predeterminado de Django

class CustomPasswordResetForm(PasswordResetForm):
    pass

class CustomSetPasswordForm(SetPasswordForm):
    pass

class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ['numero_guia', 'cliente', 'descripcion', 'estado', 'direccion_origen', 'direccion_destino']