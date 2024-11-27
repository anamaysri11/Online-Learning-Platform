






"""
Django settings for student project.




Generated by 'django-admin startproject' using Django 5.0.6.




For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/




For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""




from pathlib import Path


from datetime import timedelta








# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent








# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f#zk-lei-zu2-&((r(gl7**r)0_n%7t0avs=y2xg*+$j$i7ti8'




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True




ALLOWED_HOSTS = []




SITE_ID = 1


REST_USE_JWT = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'


# Application definition
SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
   'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
   'ROTATE_REFRESH_TOKENS': False,
   'BLACKLIST_AFTER_ROTATION': True,
   'UPDATE_LAST_LOGIN': False,
   'ALGORITHM': 'HS256',
   'VERIFYING_KEY': None,
   'AUTH_HEADER_TYPES': ('Bearer',),
   'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
   'USER_ID_FIELD': 'id',
   'USER_ID_CLAIM': 'user_id',
   'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
   'TOKEN_TYPE_CLAIM': 'token_type',
   'JTI_CLAIM': 'jti',
}


INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'rest_framework',
  'rest_framework.authtoken',
   'dj_rest_auth',
   'allauth',
   'allauth.account',
   'allauth.socialaccount',
   'dj_rest_auth.registration',
  'student_app',
]




MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'allauth.account.middleware.AccountMiddleware',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend',
   'allauth.account.auth_backends.AuthenticationBackend',
)


# AUTH_USER_MODEL = 'student_app.Person'


CACHES = {
   'default': {
       'BACKEND': 'django_redis.cache.RedisCache',
       'LOCATION': 'redis://127.0.0.1:6379/1',
       'OPTIONS': {
           'CLIENT_CLASS': 'django_redis.client.DefaultClient',
       }
   }
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'




# Optionally configure the cache timeout and other settings
CACHE_TTL = 60 * 15  # 15 minutes


REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework_simplejwt.authentication.JWTAuthentication',
       'rest_framework.authentication.TokenAuthentication',
   ],
   'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ],
   'DEFAULT_PAGINATION_CLASS': 'student_app.pagination.StandardResultsSetPagination',
   'PAGE_SIZE': 5,
}


ROOT_URLCONF = 'student.urls'




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




WSGI_APPLICATION = 'student.wsgi.application'








# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases




DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
  }
}








# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators




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
# https://docs.djangoproject.com/en/5.0/topics/i18n/




LANGUAGE_CODE = 'en-us'




TIME_ZONE = 'UTC'




USE_I18N = True




USE_TZ = True








# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/




STATIC_URL = 'static/'




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'








