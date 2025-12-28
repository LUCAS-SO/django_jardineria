from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import os
import dj_database_url
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------
# GENERAL CONFIG
# -------------------------

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

# -------------------------
# INSTALLED APPS
# -------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Storage
    'cloudinary_storage',
    'cloudinary',

    # Custom
    'jobs',

    # Rate-limiting
    'ratelimit',
]

# -------------------------
# MIDDLEWARE
# -------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Seguridad & optimización para archivos estáticos
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Seguridad custom
    'jobs.middleware.anti_bot.BlockBadUserAgentsMiddleware',
    'jobs.middleware.rate_limit.SimpleRateLimitMiddleware',
    'jobs.middleware.ip_blocker.MaliciousIPBlockerMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jardineria_app.urls'

# -------------------------
# TEMPLATES
# -------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jardineria_app.wsgi.application'

# -------------------------
# DATABASE
# -------------------------

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# -------------------------
# PASSWORD VALIDATION
# -------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------
# INTERNATIONALIZATION
# -------------------------

LANGUAGE_CODE = 'es-Ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------
# STATIC FILES
# -------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------
# MEDIA / CLOUDINARY
# -------------------------

MEDIA_URL = '/media/'
# Redundante ya que se define en CloudinaryField, pero por si acaso
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# -------------------------
# SECURITY (PRODUCCIÓN)
# -------------------------

if not DEBUG:
    # Fuerza cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # HTTPS correcto para Render
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    # Evita ataques MITM + fuerza uso de HTTPS
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Seguridad del navegador
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    CSRF_COOKIE_HTTPONLY = True

    # Protecciones adicionales
    SECURE_CONTENT_TYPE_NOSNIFF = True
    REFERRER_POLICY = "strict-origin-when-cross-origin"

# Confianza de dominios para CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# -------------------------
# FILE UPLOAD LIMITS
# -------------------------

# Evita ataques DoS por archivo gigante
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB

# -------------------------
# DEFAULT PRIMARY KEY
# -------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'