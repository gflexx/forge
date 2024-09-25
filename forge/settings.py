from datetime import timedelta
from pathlib import Path
import os, json

with open('config.json') as config_file:
	config = json.load(config_file)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config['SECRET_KEY']

AFRICAS_TALKING = config['AFRICAS_TALKING']

DEBUG = True

ON_PRODUCTION = False

ALLOWED_HOSTS = [
    "127.0.0.1", 
    "localhost",
    "forge.glitexsolutions.co.ke",
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_EXPOSE_HEADERS = [
    'Set-Cookie',
]

SITE_NAME = 'Auth'

if ON_PRODUCTION:
    CSRF_TRUSTED_ORIGINS = ['https://forge.glitexsolutions.co.ke']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',

    'users',

    'rest_framework_simplejwt',
    'rest_framework',
    'django_filters',
]

AUTH_USER_MODEL = "users.User"

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

ROOT_URLCONF = 'forge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'forge.wsgi.application'

ASGI_APPLICATION = 'forge.asgi.application'

# Database
if ON_PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config['DB_NAME'],
            'USER': config['DB_USER'],
            'PASSWORD': config['DB_PASSORD'],
            'HOST': config['DB_HOST']
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media & Static
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Email
if ON_PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config['EMAIL_HOST']
    EMAIL_PORT = config['EMAIL_PORT']
    EMAIL_HOST_USER = config['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = True 
    DEFAULT_FROM_EMAIL = config['EMAIL_HOST_USER']
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = config['EMAIL_HOST_USER']

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
