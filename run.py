"""Servidor de producción con Waitress + WhiteNoise."""

import os

from waitress import serve
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root=settings.STATIC_ROOT)

if __name__ == '__main__':
    print('Servidor iniciado en http://0.0.0.0:8000')
    serve(application, host='0.0.0.0', port=8000, threads=4)