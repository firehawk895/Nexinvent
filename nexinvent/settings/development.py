from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ja*po#q(&u)*9t@t%w^x6-#44!sg-sa($2&0mrw)b$8k6#v1ds'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = (
#     'localhost:3030',
# )
# CORS_ORIGIN_REGEX_WHITELIST = (
#     'localhost:3030',
# )

# https://docs.djangoproject.com/en/2.1/ref/settings/#databasesexit

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nexinvent',
        'USER': 'djangowalauser',
        'PASSWORD': 'merapassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}

FRONT_END_BASE_URL = "http://localhost:3000/"

TWILIO = {
    'SID': '',
    'AUTH_TOKEN': ''
}