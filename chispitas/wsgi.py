"""
WSGI config for chispitas_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chispitas.settings')

application = get_wsgi_application()
