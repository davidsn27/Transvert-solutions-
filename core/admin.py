
from django.contrib import admin
from .models import Envio
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
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

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = (
        "numero_guia",
        "remitente_nombre",
        "destinatario_nombre",
        "tipo_envio",
        "peso",
        "estado",
        "fecha_creado",
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
