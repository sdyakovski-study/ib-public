# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '----generate a new, local django secret key----'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '----db----',
        'USER': '----username----',
        'PASSWORD': '----pswd----',
        'HOST': '----hostname----',
        'PORT': '----port----',
    }
}