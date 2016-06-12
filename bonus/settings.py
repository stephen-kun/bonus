"""
Django settings for bonus project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6shobd22op0bnv2%h)&c6zz87ap#--$jw#j$b1y*4gl*91o^!p'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djconfig',
	'djcelery',		
    'weixin',
    'manager',	
    # 'haystack',
    'core',
    'topic',
    'category',
    'topic.notification',
    'topic.gift',
    'topic.unread',
    'topic.moderate',
    'comment',
   # 'joymodel',
    'comment.bookmark',
    'comment.history',
    'comment.like',
    'user',
    #'user.auth',
    #'user.admin',
    'wx',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djconfig.middleware.DjConfigMiddleware',
]

ROOT_URLCONF = 'bonus.urls'

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
                'djconfig.context_processors.config',
                'django.core.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'bonus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qubaba',
			'USER': 'root',
			'PASSWORD': 'youqiukun',
			'HOST':'',
			'PORT':'3306'
    }
}


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

#LANGUAGE_CODE = 'zh-Hans' 

LANGUAGES = (
	('zh-Hans', 'Chinese'),
	('en', 'English'),
)

LOCALE_PATHS = (
	os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
import os
SITE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
	('css', os.path.join(STATIC_ROOT, 'css')),
	('js', os.path.join(STATIC_ROOT, 'js')),
	('images', os.path.join(STATIC_ROOT, 'images')),
]



MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/stephen/media'

COMMENT_MAX_LEN = 140
YT_PAGINATOR_PAGE_RANGE = 30

JOY_TOPIC_PRIVATE_CATEGORY_PK=1
JOY_UNICODE_SLUGS = False

RATELIMIT_ENABLE = True
RATELIMIT_CACHE_PREFIX = 'joy'
RATELIMIT_CACHE = 'default'

LOGIN_URL = 'user:auth:login'
LOGIN_REDIRECT_URL = 'user:update'

AUTHENTICATION_BACKENDS = [
    'topic.auth.AuthBackend',
    'user.auth.backends.UsernameAuthBackend',
    'user.auth.backends.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ALLOWED_UPLOAD_IMAGE_FORMAT = ('jpeg', 'png', 'gif')


NOTIFICATIONS_PER_PAGE = 20


MENTIONS_PER_COMMENT = 30

USER_LAST_SEEN_THRESHOLD_MINUTES = 1


ALLOWED_URL_PROTOCOLS = {
    'http', 'https', 'mailto', 'ftp', 'ftps',
    'git', 'svn', 'magnet', 'irc', 'ircs'}


UNIQUE_EMAILS = True
CASE_INSENSITIVE_EMAILS = True

# SESSION_COOKIE_AGE=60*30
# SESSION_EXPIRE_AT_BROWSER_CLOSE=False
# SESSION_COOKIE_DOMAIN = ['*',]

TICKET_URL = "wx.tonki.com.cn/manager/account/send_coupon/"

import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_RESULT_EXPIRES=3600

IMAGE_OPTIMIZE= 0.5
IMAGE_QUALITY = 70
MIN_COMPRESS_IMAGE_SIZE = 100*1024
