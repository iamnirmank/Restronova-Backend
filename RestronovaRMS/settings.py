import os
from pathlib import Path
import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default=get_random_secret_key())
SECRET_KEY = "django-insecure-mic+=r5g_!g^oe)a*-tkiblimnvf2n5biew&!!kefj)8j$)mb!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set this to False in production.

# ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split()
ALLOWED_HOSTS = ['djangoapp-69350.azurewebsites.net', 'localhost', "127.0.0.1", '127.0.0.1:5173']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'daphne',

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'allauth',
    'allauth.account',

    "InventoryApp",
    "AuthApp",

    "rest_framework",
    "drf_yasg",
    'corsheaders',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "RestronovaRMS.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'postgres'),
        'USER': os.environ.get('DJANGO_DB_USER', 'Terraform@mydjangoserver-69350.postgres.database.azure.com'),  
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'Database2024'),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'mydjangoserver-69350.postgres.database.azure.com'),
        'PORT': os.environ.get('DJANGO_DB_PORT', '5432'),
    }
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5174',
    'https://restronovarms.vercel.app',
    'https://inventoryappbackend.azurewebsites.net',
    'http://127.0.0.1:5173',
    'https://restronova.capitechnepal.com',
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_ASYNC = True

# Static files
STATIC_URL = "static/"
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'work.sikify@gmail.com'
EMAIL_HOST_PASSWORD = 'qulhnqzjmklbtals'

# Allauth settings
EMAIL_VERIFICATION = 'mandatory'

AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=bajarify;AccountKey=tCAO++q56kgXWPT5seziz04z38AjRpQqixjA5eRvH6Tfm/dzkqO60J2tUzPzyY4W+nzUigaXijfB+AStaQ2sYw==;EndpointSuffix=core.windows.net'

AUTH_USER_MODEL = 'AuthApp.User'

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_INFO': {
        'title': 'RestonovaAPIs',
        'version': '1.0.0',
    },
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}

# Swagger settings
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ASGI application
ASGI_APPLICATION = "RestronovaRMS.asgi.application"

# Channels layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}