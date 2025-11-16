from django import forms
from .models import Envio

class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ['origen', 'destino', 'descripcion']
