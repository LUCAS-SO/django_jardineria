from django.core.cache import cache
from django.http import HttpResponseForbidden

class MaliciousIPBlockerMiddleware:
    BLOCK_TIME = 60 * 60  # 1 hora
    MAX_404 = 20          # si una IP hace más de 20 errores 404

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "unknown")

        # ¿Está bloqueada?
        if cache.get(f"blocked:{ip}"):
            return HttpResponseForbidden("Forbidden")

        response = self.get_response(request)

        if response.status_code == 404:
            key = f"404:{ip}"
            count = cache.get(key, 0) + 1
            cache.set(key, count, timeout=3600)

            # Si supera el límite → bloqueo IP
            if count >= self.MAX_404:
                cache.set(f"blocked:{ip}", True, timeout=self.BLOCK_TIME)
                return HttpResponseForbidden("Forbidden")

        return response
