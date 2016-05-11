"""
Django settings for ibpublic project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

import secret_settings

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# settings.py will be read and evaluated on the project level (possibly by manage.py).
# BASE_DIR points to the '/home/sdyakovski/projects/python-projects/ib-public/project'
# but is dealing with relative paths, not absolute paths, so its value from manage.py would be ''.
# It simply starts with __file__ (which is settings.py); its dirname (ibpublic); and its dirname (project),
# which is the curdir of manage.py => '' 

# ADD EXTERNALS PATHS TO sys.path
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# BASE_PATH is abspath of 'ibpublic/..', which is 
# '/home/sdyakovski/projects/python-projects/ib-public/project'
# - which is the same dir as BASE_DIR, but absolute (needed for sys.path)
EXTERNAL_LIBS_PATH = os.path.join(BASE_PATH, 'externals', 'libs')
EXTERNAL_APPS_PATH = os.path.join(BASE_PATH, 'externals', 'apps')
sys.path = ['', EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path[1:]
# [1:] in order to eliminate the first element of the list (''), which is moved to the front

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
# PROJECT_PATH is abspath of 'ibpublic', where __file__ (settings.py) is, which is 
# '/home/sdyakovski/projects/python-projects/ib-public/project/ibpublic'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'rater.apps.RaterConfig',
    'utils.apps.UtilsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'localflavor',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ibpublic.urls'

TEMPLATES = [
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
            ],
        },
    },
]

WSGI_APPLICATION = 'ibpublic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES =     secret_settings.DATABASES


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
