from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
import time

class SimpleRateLimitMiddleware:
    RATE = 100   # requests
    WINDOW = 60  # segundos

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "unknown")
        key = f"rl:{ip}"
        data = cache.get(key, {"count": 0, "start": time.time()})

        # Reiniciar ventana
        if time.time() - data["start"] > self.WINDOW:
            data = {"count": 0, "start": time.time()}

        data["count"] += 1
        cache.set(key, data, timeout=self.WINDOW)

        if data["count"] > self.RATE:
            return HttpResponseTooManyRequests("Too many requests")

        return self.get_response(request)
