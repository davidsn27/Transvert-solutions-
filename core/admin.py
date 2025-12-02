from django.contrib import admin
# IMPORTAR TODOS LOS MODELOS NECESARIOS
from .models import (
    Envio, TrazaEnvio, SoporteTicket, SoporteRespuesta, 
    Zona, Tarifa # Modelos de Tarificación y Zonas
) 
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 🔥 1. Desregistrar el User original
admin.site.unregister(User)


# 🔥 2. Registrar tu UserAdmin personalizado
@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("-date_joined",)

    # 🔒 Bloquear eliminación TOTAL de usuarios
    def has_delete_permission(self, request, obj=None):
        return False

    # 🔒 Impedir que un admin se desactive solo
    def save_model(self, request, obj, form, change):
        if obj == request.user and not obj.is_active:
            raise ValueError("No puedes desactivar tu propia cuenta.")
        super().save_model(request, obj, form, change)

    # 🔥 3. ACCIONES: activar / desactivar usuarios
    actions = ["activar_usuarios", "desactivar_usuarios"]

    def activar_usuarios(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Usuarios activados correctamente.")

    activar_usuarios.short_description = "Activar usuarios seleccionados"

    def desactivar_usuarios(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Usuarios desactivados correctamente.")

    desactivar_usuarios.short_description = "Desactivar usuarios seleccionados"

# ---------------------------------------------
# CONFIGURACIÓN DE ENVÍOS Y TRAZABILIDAD
# ---------------------------------------------

# INLINE para mostrar el historial de trazabilidad dentro del Envío
class TrazaEnvioInline(admin.TabularInline):
    model = TrazaEnvio
    extra = 0
    readonly_fields = ('usuario', 'fecha_hora', 'estado_anterior') 

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = (
        "numero_guia",
        "estado", # <-- Columna estado movida para mejor visibilidad
        "remitente_nombre",
        "destinatario_nombre",
        "tipo_envio",
        "peso",
        "fecha_creado",
        "usuario", # <-- Muestra el usuario que lo creó
    )

    list_filter = ("estado", "tipo_envio", "fecha_creado")

    search_fields = (
        "numero_guia",
        "remitente_nombre",
        "destinatario_nombre",
        "remitente_telefono",
        "destinatario_telefono",
        "direccion_origen",
        "direccion_destino",
    )

    ordering = ("-fecha_creado",)

    readonly_fields = ("fecha_creado",)
    
    inlines = [TrazaEnvioInline] # <-- AÑADIDO: Muestra la trazabilidad


# ---------------------------------------------
# CONFIGURACIÓN DE SOPORTE (NUEVO REGISTRO)
# ---------------------------------------------

# INLINE para mostrar las respuestas dentro del Ticket
class SoporteRespuestaInline(admin.StackedInline):
    model = SoporteRespuesta
    extra = 1

@admin.register(SoporteTicket)
class SoporteTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'asunto', 'usuario', 'estado', 'prioridad', 'fecha')
    list_filter = ('estado', 'prioridad', 'fecha')
    search_fields = ('asunto', 'descripcion', 'usuario__username')
    inlines = [SoporteRespuestaInline] # <-- AÑADIDO: Muestra las respuestas


# ---------------------------------------------
# REGISTROS DE TARIFAS (NUEVOS)
# ---------------------------------------------

# Se registran los modelos de Tarificación y Zona/Ciudad
admin.site.register(Zona)
admin.site.register(Tarifa)
