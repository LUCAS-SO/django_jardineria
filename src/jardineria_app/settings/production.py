from .base import *
import dj_database_url

DEBUG = False

render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
ALLOWED_HOSTS = [render_host] if render_host else []

# -------------------------
# DATABASE (PROD)
# -------------------------

DATABASES = {
    "default": dj_database_url.parse(
        os.environ["DATABASE_URL"],
        conn_max_age=600,
        ssl_require=True,
    )
}

# -------------------------
# SECURITY
# -------------------------

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
REFERRER_POLICY = "strict-origin-when-cross-origin"

X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_HTTPONLY = True

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]
