"""
Django settings for home project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST", cast=str, default=None)
EMAIL_PORT = config("EMAIL_PORT", cast=str, default='587') # Recommended
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)  # Use EMAIL_PORT 587 for TLS
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)  # EUse MAIL_PORT 465 for SSL

ADMIN_USER_NAME=config("ADMIN_USER_NAME", default="Admin user")
ADMIN_USER_EMAIL=config("ADMIN_USER_EMAIL", default=None)

MANAGERS=[]
ADMINS=[]
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS +=[
        (f'{ADMIN_USER_NAME}', f'{ADMIN_USER_EMAIL}')
    ]
    MANAGERS=ADMINS


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    #myapps
    'ads',
    'apis',

    #third party apps
    'allauth_ui',
    'allauth',    
    'allauth.account',
    'allauth.socialaccount',
    'widget_tweaks',
    'slippers',
    'rest_framework',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",    
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#django allouth config
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Ad-Ventures]"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
ALLAUTH_UI_THEME = "coffee"

AUTHENTICATION_BACKENDS = [   
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',    
]
WSGI_APPLICATION = 'home.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_BASE_DIR = BASE_DIR / "staticfiles"
STATICFILES_BASE_DIR.mkdir(exist_ok=True, parents=True)
STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / "vendors"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
