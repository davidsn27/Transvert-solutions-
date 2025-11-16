from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Panel de Administración - TRANSVERT"
admin.site.site_title = "Admin TRANSVERT"
admin.site.index_title = "Bienvenido al panel de control"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # tu app principal
]