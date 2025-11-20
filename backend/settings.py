"""
Django settings for transvert_solutions project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tu_clave_secreta'  # ¡CAMBIA ESTO EN PRODUCCIÓN!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # ¡CAMBIA A False EN PRODUCCIÓN!

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core',  # Tu aplicación 'core'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'backend.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Agrega la carpeta 'templates' en la raíz del proyecto
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
            
        },
    }
]
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Puedes usar otro motor de base de datos (ej. PostgreSQL)
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'  # Cambia al idioma que prefieras

TIME_ZONE = 'America/Bogota'  # Cambia a tu zona horaria

USE_I18N = True
USE_L10N = True 

USE_TZ = True

# Static files (CSS, JavaScript, Images)k
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Ruta de archivos estáticos
STATIC_URL = '/static/'

# Carpeta donde estarán tus archivos CSS, JS, imágenes
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Opcional, para producción
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'tu_servidor_smtp.com'  # Cambia esto
EMAIL_PORT = 587  # o 465 si usas SSL
EMAIL_USE_TLS = True  # o EMAIL_USE_SSL = True si usas SSL
EMAIL_HOST_USER = 'tu_correo@example.com'  # Cambia esto
EMAIL_HOST_PASSWORD = 'tu_contraseña'  # Cambia esto
DEFAULT_FROM_EMAIL = 'tu_correo@example.com'  # Cambia esto

# Redirect URLs
LOGIN_REDIRECT_URL = 'index'  # Redirige al 'index' después del inicio de sesión
LOGOUT_REDIRECT_URL = 'index'  # Redirige al 'index' después del cierre de sesión

# Configuración de la API de Google Maps
GOOGLE_MAPS_API_KEY = "AIzaSyABUjqnn42gv2L6Re4eNjRj_QQHjDbwQjc"  # ¡CAMBIA ESTO!

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
# Configuración de CORS
CORS_ALLOWED_ORIGINS = [
    "https://tu_dominio_cliente.com",
    "http://localhost:3000",  # Ejemplo para desarrollo
]
