from django.http import HttpResponseForbidden

BLOCKED_AGENTS = [
    "curl", "wget", "python-requests", "scrapy",
    "nmap", "sqlmap", "masscan", "gobuster"
]

class BlockBadUserAgentsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        agent = request.META.get("HTTP_USER_AGENT", "").lower()

        if any(bad in agent for bad in BLOCKED_AGENTS):
            return HttpResponseForbidden("Forbidden")

        return self.get_response(request)
