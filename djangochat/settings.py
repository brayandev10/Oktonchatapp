from pathlib import Path
import os
import socket

IS_PYTHONANYWHERE = socket.gethostname().endswith('pythonanywhere.com')
#stripe payement

from dotenv import load_dotenv

load_dotenv()

CINETPAY_API_KEY = "votre_api_key"
CINETPAY_SITE_ID = "105895780"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOGIN_URL = '/login/'  # Remplace par ton URL réelle de connexion
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'brayantematio1@gmail.com'
EMAIL_HOST_PASSWORD = 'failyfuerqybghxz'
DEFAULT_FROM_EMAIL = 'brayantematio1@gmail.com'
# En production, configure un vrai serveur SMTP (Gmail, Mailgun, etc.)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0z!zh^axu+2u^6mx91=af(z#7svevunwano(6mz7)yrtw71eog'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'social_django',
    'chat',
    'pwa',
    'payments',
    'whitenoise.middleware.WhiteNoiseMiddleware',
  #  'webpush'
]



AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Clés Google OAuth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '22370549515-9q1p6fc4u48gcbn59d8pgbndvushq2j2.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # Remplace-le par ton vrai secret

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'





PWA_APP_NAME = 'CodeZone'
PWA_APP_DESCRIPTION = "communauté de codeZone , collaboration, partage et code plus plus"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/Icone/icone.png',
        'sizes': '512x512'
    }
]
PWA_APP_DIR = 'ltr'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]




ROOT_URLCONF = 'djangochat.urls'

TEMPLATES = [
    {
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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


#DATABASES = {
#    'default': {
       # 'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'mydb',
#        'USER': 'mydb',
#        'PASSWORD': 'storm,1234',
#        'HOST': 'localhost',
#        'PORT': '',
#    }
#}

WSGI_APPLICATION = 'djangochat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

if IS_PYTHONANYWHERE:
    MEDIA_URL = '/chat_files/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media', 'chat_files')
else:
    MEDIA_URL = '/media/chat_files/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media', 'chat_files')
    


# Fichiers statiques (CSS, JS, sons, images...)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # pour collectstatic en production


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
