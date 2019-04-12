"""
* Purpose:  Settings
* @author: Nikhil Lad
* @version: 3.7
* @since: 01-1-2019
"""
import os
import datetime
from dotenv import load_dotenv
from pathlib import Path  # python3 only
from celery.schedules import crontab


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# Quick-start development settings - unsuitable for production


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','localhost']

#Email verification
EMAIL_USE_TLS = True            # Email Tools true
EMAIL_PORT = 587                                       # default email port
EMAIL_HOST=os.getenv("EMAIL_HOST")  # SMTP protocol for gmail
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')    # email to be send from user
EMAIL_HOST_PASSWORD =os.getenv('EMAIL_HOST_PASSWORD')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'guardian.backends.ObjectPermissionBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
)

# Application definition

INSTALLED_APPS = [
    'apidemo',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',

    'rest_framework.authentication',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework_swagger',
    'social_django',
    'django_celery_beat',
    'django_elasticsearch_dsl',

]

ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },

}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SITE_ID = 1

MIDDLEWARE = [
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
   # 'django.middleware.cache.FetchFromCacheMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'restapi_demo.urls'


TEMPLATES = [
 {
   'BACKEND': 'django.template.backends.jinja2.Jinja2',
   'DIRS': [],
   'APP_DIRS': True,
   'OPTIONS': {
     'environment': 'restapi_demo.jinja2.environment'
   },
 },
 {
   'BACKEND': 'django.template.backends.django.DjangoTemplates',
   'DIRS': [],
   'APP_DIRS': True,
   'OPTIONS': {
     'context_processors': [
       'django.template.context_processors.debug',
       'django.template.context_processors.request',
       'django.contrib.auth.context_processors.auth',
       'django.contrib.messages.context_processors.messages',
        'social_django.context_processors.backends',  # <--
        'social_django.context_processors.login_redirect',
     ],
   },
 },
]


WSGI_APPLICATION = 'restapi_demo.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.getenv("DATABASE_ENGINE"),
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': '',
    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_SECURE = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


CACHES = {
    "default": {
        "BACKEND": os.getenv("REDIS_BACKEND"),
        "LOCATION": os.getenv("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": os.getenv("REDIS_CLIENT_CLASS"),
        }
    }
}

CACHE_TTL = 60 * 15     # Cache time to live is 15 minutes.



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ],
        'TEST_REQUEST_DEFAULT_FORMAT':'json',
        "DATE_INPUT_FORMATS": ["%m-%d-%Y"],
}



JWT_AUTH = {

    'JWT_VERIFY': True,             #It will raise a jwt.DecodeError if the secret is wrong.
    'JWT_VERIFY_EXPIRATION': True,  # Tokens will expire after a period of time. The default time is five minutes.
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',   #  value prefix that is required to be sent together with the token. We have set it as Bearer, and the default is JWT.

}

LOGIN_URL = '/login_v'
LOGIN_REDIRECT_URL = '/base'
LOGOUT_URL = '/logout'

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }

    }

}

SOCIAL_AUTH_URL_NAMESPACE = 'social'
# social authentication keys

SOCIAL_AUTH_GITHUB_KEY =os.getenv("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("SOCIAL_AUTH_GITHUB_SECRET")

SOCIAL_AUTH_FACEBOOK_KEY= os.getenv("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET =os.getenv("SOCIAL_AUTH_FACEBOOK_SECRET")

SOCIAL_AUTH_TWITTER_KEY =os.getenv("SOCIAL_AUTH_TWITTER_KEY")
SOCIAL_AUTH_TWITTER_SECRET = os.getenv("SOCIAL_AUTH_TWITTER_SECRET")

#CELERY_BROKER_URL = 'redis://localhost:6379'

CELERY_BROKER_URL ='amqp://localhost'       # rabbit-mq as message broker

CELERY_TIMEZONE = "Asia/Kolkata"

# SCHEDULE for tasks
CELERY_BEAT_SCHEDULE = {
    'auto_delete_archive_and_trash': {
        'task': 'apidemo.tasks.auto_delete_archive_and_trash',
        'schedule': crontab(minute=0, hour=10),
        'args': 49
    }
}
