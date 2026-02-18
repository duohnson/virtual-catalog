import time
import logging
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware:
    """
    Agrega cabeceras HTTP de seguridad a cada respuesta.
    Protege contra ataques XSS, clickjacking, sniffing de contenido
    y fuerza el uso de HTTPS cuando está habilitado.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        return response


class RequestTimingMiddleware:
    """
    Mide el tiempo de procesamiento de cada request y lo registra
    en los logs. Útil para detectar endpoints lentos.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        if duration > 1.0:
            logger.warning(
                'Request lento: %s %s (%.2fs)',
                request.method,
                request.get_full_path(),
                duration
            )

        return response


class RateLimitMiddleware:
    """
    Limitador de peticiones básico en memoria.
    Restringe la cantidad de requests por IP en un intervalo de tiempo
    para prevenir abuso de endpoints.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}
        self.max_requests = getattr(settings, 'RATE_LIMIT_MAX_REQUESTS', 100)
        self.window = getattr(settings, 'RATE_LIMIT_WINDOW', 60)

    def __call__(self, request):
        if settings.DEBUG:
            return self.get_response(request)

        ip = self._get_client_ip(request)
        now = time.time()

        if ip in self.requests:
            requests_list = self.requests[ip]
            requests_list = [t for t in requests_list if now - t < self.window]
            self.requests[ip] = requests_list

            if len(requests_list) >= self.max_requests:
                logger.warning('Rate limit alcanzado para IP: %s', ip)
                return JsonResponse(
                    {'error': 'Demasiadas solicitudes. Intenta de nuevo más tarde.'},
                    status=429
                )

        self.requests.setdefault(ip, []).append(now)
        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')
