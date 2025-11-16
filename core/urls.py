from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('superadmin/', views.superadmin_panel, name='superadmin_panel'),  # 🔥 nueva ruta
    path('contact/', views.about_view, name='contact'),
    path('logout/', views.logout_view, name='logout'),
    path('seguimiento/', views.seguimiento_view, name='seguimiento'),
    path('crear-envio/', views.crear_envio, name='crear_envio'),
    path('staff_panel/', views.staff_panel, name='staff_panel'),
    path('actualizar_estado_envio/', views.actualizar_estado_envio, name='actualizar_estado_envio'),
]
