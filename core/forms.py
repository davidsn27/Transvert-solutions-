from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Envio

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd.get('password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ['cliente', 'direccion_origen', 'direccion_destino', 'descripcion']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_origen': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_destino': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
