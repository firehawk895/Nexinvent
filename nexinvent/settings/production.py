from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

TWILIO = {
    'SID': os.environ['TWILIO_SID'],
    'AUTH_TOKEN': os.environ['TWILIO_AUTH_TOKEN']
}

DEBUG = os.environ['DEBUG']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = (
#     'dev.orderclap.com',
#     'app.orderclap.com'
# )
# CORS_ORIGIN_REGEX_WHITELIST = (
#     'localhost:3030',
# )

# https://docs.djangoproject.com/en/2.2/ref/settings/#secure-ssl-redirect
# force ssl redirect
SECURE_SSL_REDIRECT = True

# You need this for Elastic Beanstalk or you'll get infinite redirects
# https://rickchristianson.wordpress.com/2013/10/31/getting-a-django-app-to-use-https-on-aws-elastic-beanstalk/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

FRONT_END_BASE_URL = os.environ['FRONT_END_BASE_URL']
