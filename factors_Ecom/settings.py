from pathlib import Path
import os
from decouple import config
import dj_database_url
import cloudinary

# ================= BASE =================

BASE_DIR = Path(__file__).resolve().parent.parent

# ================= SECURITY =================

SECRET_KEY = config('SECRET_KEY', default='unsafe-secret-key')

# IMPORTANT: local .env → DEBUG=True
# render .env → DEBUG=False
DEBUG = config('DEBUG', default=True, cast=bool)


# ================= HOST & CSRF =================

if DEBUG:
    # Local development
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
    ]

    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1',
        'http://localhost',
    ]

else:
    # Render production
    ALLOWED_HOSTS = [
        'pacific-mart.onrender.com',
        '.onrender.com',
        'localhost',
        '127.0.0.1',
    ]

    CSRF_TRUSTED_ORIGINS = [
        'https://pacific-mart.onrender.com',
        'https://*.onrender.com',
    ]


# IMPORTANT FOR RENDER PROXY
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Only redirect HTTPS in production
SECURE_SSL_REDIRECT = False if DEBUG else True


# ================= APPS =================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps
    'category',
    'accounts',
    'product',
    'cart',
    'orders',
    'bkash',
    'nagad',
    'cashOnDelevery',

    # third party
    'widget_tweaks',
    'cloudinary',
    'cloudinary_storage',
]


# ================= MIDDLEWARE =================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # whitenoise must be directly after security
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================= URLS =================

ROOT_URLCONF = 'factors_Ecom.urls'


# ================= TEMPLATES =================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # custom processors
                'category.context_processors.menu_links',
                'cart.context_processors.counter',
            ],
        },
    },
]


# ================= WSGI =================

WSGI_APPLICATION = 'factors_Ecom.wsgi.application'


# ================= DATABASE =================

DATABASE_URL = config(
    'DATABASE_URL',
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
)

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}


# ================= AUTH =================

AUTH_USER_MODEL = 'accounts.Account'


# ================= PASSWORD VALIDATORS =================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ================= INTERNATIONAL =================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# ================= STATIC =================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'factors_Ecom' / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ================= MEDIA (Cloudinary) =================

MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


CLOUDINARY_STORAGE = {

    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),

    'API_KEY': config('CLOUDINARY_API_KEY'),

    'API_SECRET': config('CLOUDINARY_API_SECRET'),

}


cloudinary.config(

    cloud_name=config('CLOUDINARY_CLOUD_NAME'),

    api_key=config('CLOUDINARY_API_KEY'),

    api_secret=config('CLOUDINARY_API_SECRET'),

)


# ================= SESSION =================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_AGE = 1209600

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SAMESITE = 'Lax'

SESSION_SAVE_EVERY_REQUEST = False


# ================= CSRF =================

CSRF_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_AGE = 31449600

CSRF_COOKIE_SAMESITE = 'Lax'


# ================= EMAIL =================

EMAIL_HOST = config('EMAIL_HOST')

EMAIL_PORT = config('EMAIL_PORT', cast=int)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)


# ================= MESSAGE TAGS =================

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {

    messages.ERROR: "danger"

}


# ================= DEFAULT =================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
