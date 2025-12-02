from pathlib import Path
import os

# --------------------------------------------------
# BASE DEL PROYECTO
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SEGURIDAD
# --------------------------------------------------
SECRET_KEY = 'django-insecure-tu_clave_secreta'
DEBUG = True
# MANTENIDO: Clave para que el servidor sea accesible en la red local (portabilidad)
ALLOWED_HOSTS = ['*'] 


# --------------------------------------------------
# APLICACIONES
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'core',
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
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


# --------------------------------------------------
# URLS Y WSGI
# --------------------------------------------------
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'backend.wsgi.application'


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]


# --------------------------------------------------
# BASE DE DATOS
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------------------------------------
# VALIDACIÓN DE CONTRASEÑAS
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------------
# IDIOMA Y ZONA HORARIA
# --------------------------------------------------
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# ARCHIVOS ESTÁTICOS
# --------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# --------------------------------------------------
# ARCHIVOS MULTIMEDIA
# --------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------
# CLAVE PRIMARIA POR DEFECTO
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------
# LOGIN Y LOGOUT
# --------------------------------------------------
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'


# --------------------------------------------------
# GOOGLE MAPS (OPCIONAL)
# --------------------------------------------------
GOOGLE_MAPS_API_KEY = "AIzaSyABUjqnn42gv2L6Re4eNjRj_QQHjDbwQjc"


# --------------------------------------------------
# DJANGO REST FRAMEWORK
# --------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}


# --------------------------------------------------
# CORS
# --------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]


# --------------------------------------------------
# CONFIGURACIÓN DE EMAIL (RECUPERACIÓN DE CONTRASEÑA)
# --------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"

# MODIFICACIÓN CRUCIAL PARA MAYOR ESTABILIDAD CON GMAIL
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_HOST_USER = "transvert.solutions.enterprice@gmail.com"
EMAIL_HOST_PASSWORD = "ecbybutztbvmvzcz" # Asegúrate de que esta es una Contraseña de Aplicación

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PASSWORD_RESET_TIMEOUT = 900


# --------------------------------------------------
# DOMINIO PARA ENLACES DE CORREO
# --------------------------------------------------
# IMPORTANTE: Reemplaza esta IP con la IP LOCAL REAL de tu PC antes de enviar el correo.
DEFAULT_DOMAIN = "172.30.3.122:8000"


# --------------------------------------------------
# SITE ID
# --------------------------------------------------
SITE_ID = 1


# --------------------------------------------------
# CLAVE DE GEMINI API (ADICIÓN PARA CHATBOT)
# --------------------------------------------------
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyD1QcU9uW7JSVKYBBMsqCaxLiPg2QZ5srs')
