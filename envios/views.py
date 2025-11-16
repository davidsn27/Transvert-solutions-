from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EnvioForm

@login_required
def crear_envio(request):
    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            envio = form.save(commit=False)
            envio.cliente = request.user
            envio.save()
            return render(request, 'envios/envio_exitoso.html', {'envio': envio})
    else:
        form = EnvioForm()
    return render(request, 'envios/crear_envio.html', {'form': form})
