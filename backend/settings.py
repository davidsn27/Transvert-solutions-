import os
from pathlib import Path

# 🏗️ BASE_DIR es la ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚙️ Configuración básica
SECRET_KEY = 'django-insecure-12345-transvert-key-67890' 
DEBUG = True
ALLOWED_HOSTS = [] 

# 📦 Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', 
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# 🧠 Configuración WSGI
WSGI_APPLICATION = 'backend.wsgi.application'

# 🗄️ Base de datos SQLite (puedes cambiar a MySQL 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 Validaciones de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Idioma y zona horaria
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# 🧾 Archivos estáticos (CSS, imágenes, JS)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core', 'static'),
]
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# 📦 Archivos subidos por el usuario
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🪪 ID del campo por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 🔐 Configuración de autenticación
LOGIN_URL = 'login'  
LOGIN_REDIRECT_URL = 'home'  
LOGOUT_REDIRECT_URL = 'index'  