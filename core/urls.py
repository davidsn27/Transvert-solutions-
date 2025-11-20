from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('staff_panel/', views.staff_panel, name='staff_panel'),
    path('superadmin_panel/', views.superadmin_panel, name='superadmin_panel'),
    path('actualizar_estado_envio/', views.actualizar_estado_envio, name='actualizar_estado_envio'),
    path('seguimiento/', views.seguimiento_envio, name='seguimiento_envio'),
    path('crear-envio/', views.crear_envio, name='crear_envio'),
    path('api/crear-envio/', views.crear_envio_api, name='crear_envio_api'),

    # ==========================
    # RESTABLECER CONTRASEÑA (OFICIAL DJANGO)
    # ==========================
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset_form.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
            success_url='done/'
        ),
        name='password_reset'
    ),

    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url='/reset/done/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
