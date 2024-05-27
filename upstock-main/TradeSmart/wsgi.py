"""
WSGI config for TradeSmart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add the project directory to the sys.path
sys.path.append('/home/Mystery700/upstock')

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradeSmart.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

