"""
WSGI config for djangochat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv  # 1. Charger les variables d'environnement d'abord

load_dotenv()  # Charge .env (doit être placé avant l'initialisation Django)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangochat.settings')

application = get_wsgi_application()