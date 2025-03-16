from .base import *


ALLOWED_HOSTS = ['*']
ALLOWED_SIGNUP_DOMAINS = ['*']
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "localhost",
    # ...
]

MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE


# WSGI_APPLICATION = 'config.wsgi.application'
# ASGI_APPLICATION = 'config.asgi.application'



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ASGI_APPLICATION = 'config.routing.application'
# Email
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "./tmp/app-messages"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025


 
# Cache
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": ""
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR/'caches',
        'TIMEOUT': 6,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}



CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # 'CONFIG': {'hosts': ['localhost', 6379],}
}}

# CHANNEL_LAYERS={
#     'default': {
#         'BACKEND':'channels_redis.core.RedisChannelLayer',
#         'CONFIG':{
#             'hosts': [('localhost', 6379)],
#         }
#     },
# }


# import environ

# ROOT_DIR = environ.Path(__file__) - 3

# Static files
# STATIC_ROOT = str(BASE_DIR('staticfiles'))
STATIC_URL = '/static/'
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# ]




# Media
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

DATA_UPLOAD_MAXMEMORY_SIZE = 104857600  # 10MB shall be the maximum size of a file upload in th esite to maximize storage


LOGIN_REDIRECT_URL = 'home:home'
LOGIN_URL = 'login'


STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, "../asset")
# STATICFILES_DIRS = [
#        os.path.join(BASE_DIR, "../assets"),
#   ]


LOGIN_URL = '/login/' 

print(MEDIA_ROOT)