from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Panel de Administración - TRANSVERT"
admin.site.site_title = "Admin TRANSVERT"
admin.site.index_title = "Bienvenido al panel de control"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ✅ Tu app principal
    path('password-reset/', include('django.contrib.auth.urls')),
]

# ✅ ESTO SIEMPRE VA DESPUÉS DE HABER DEFINIDO urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
