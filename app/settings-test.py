"""
Django settings for acgroup-incity-apis project.
Generated by 'django-admin startproject' using Django 2.0.4.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from django.contrib.messages import constants as message_constants
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l&2vv7_nfm5#tjy!o0zdp^#5is)86%)%*$)-o^c+s1y#68!g0%'

# App Directory
APP_DIR = 'acgroup-incity-apis'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_LOCAL = False

if IS_LOCAL:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    '127.0.0.1',
]

# SECURE_HSTS_SECONDS = 86400
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_PRELOAD = True

# Application definition

INSTALLED_APPS = [
    # apps
    'app',
    'backend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # db app logger
    # 'django_db_logger',
    # static css and js compressor
    'compressor',
    # google recaptcha
    'captcha',
    # user agent details
    'django_user_agents',
    # datatable
    'django_tables2',
    # debug toolbar
    # 'debug_toolbar',
    # django_archive
    'django_archive',
    # django_tinymce
    'tinymce',
    # # cors
    # 'corsheaders',
    # Bootstrap Modals
    'bootstrap_modal_forms',
    # 'background-task',
    'prettyjson',
]

TEMPLATE_PATH_BACKEND = 'backend/'
TEMPLATE_PATH_FRONTEND = 'frontend/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # other middleware
    'django_user_agents.middleware.UserAgentMiddleware',
    # debug toolbar
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # # cors
    # 'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'app.urls'

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
                # app global constants
                'app.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

APP_DOMAIN_LOCAL = 'http://127.0.0.1:8000'
APP_DOMAIN_PROD = 'https://card-test.tapandgoticketing.co.rw'
LOGO_URL_LOCAL = APP_DOMAIN_LOCAL
LOGO_URL_PROD = APP_DOMAIN_PROD
BACKEND_DOMAIN_LOCAL = APP_DOMAIN_LOCAL+'/backend'
BACKEND_DOMAIN_PROD = APP_DOMAIN_PROD+'/backend'
FRONTEND_DOMAIN_LOCAL = APP_DOMAIN_LOCAL+'/frontend'
FRONTEND_DOMAIN_PROD = APP_DOMAIN_PROD+'/frontend'
STATIC_LOCAL = APP_DOMAIN_LOCAL+'/static/'
STATIC_PROD = APP_DOMAIN_PROD+'/static/'
# Redirect
LOGIN_URL = '/' + APP_DIR + '/operators/signin'
CONTACT_URL = 'https://acgroup.rw'

if IS_LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_tap_and_go_ticketing',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'traditional',
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_tap_and_go_ticketing',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'sql_mode': 'traditional',
            }
        }
    }

ARCHIVE_DIRECTORY = 'backups'
ARCHIVE_FILENAME = '%Y-%m-%d-%H-%M-%S'
ARCHIVE_FORMAT = 'bz2'  # gz, bz2
ARCHIVE_EXCLUDE = (
    'contenttypes.ContentType',
    'sessions.Session',
    'auth.Permission',
    'app.Backups',
)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Datetime
USE_TZ = True
TIME_IN_SECONDS = True
TIME_ZONE = 'UTC'
TIME_DIFFERENCE = -2*3600
APP_CONSTANT_DISPLAY_TIME_ZONE = 'Africa/Kigali'
APP_CONSTANT_DISPLAY_TIME_ZONE_INFO = '(CAT)'
APP_CONSTANT_DISPLAY_DATE_FORMAT = '%a, %d %b %Y'
APP_CONSTANT_DISPLAY_TIME_FORMAT = '%H:%M:%S'
APP_CONSTANT_DISPLAY_DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S'
APP_CONSTANT_DISPLAY_DATETIME_FORMAT_OTHER = '%d %b %Y %H:%M:%S'
APP_CONSTANT_INPUT_DATE_FORMAT = '%Y-%m-%d'
APP_CONSTANT_INPUT_TIME_FORMAT = '%H:%M:%S'
APP_CONSTANT_INPUT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
APP_CONSTANT_DEFAULT_DATETIME = '0001-01-01 00:00:00'
APP_CONSTANT_DEFAULT_DATE = '0001-01-01'
APP_CONSTANT_DEFAULT_TIME = '00:00:00'
APP_CONSTANT_DEFAULT_DATETIME_VALUE = '0001-01-01 00:00:00'
APP_CONSTANT_DEFAULT_DATE_VALUE = '0001-01-01'

USE_I18N = True

USE_L10N = True

MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

if IS_LOCAL:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = '/static/'
    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = '/static/'
    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = 'compressor.storage.CompressorFileStorage'
COMPRESS_OUTPUT_DIR = 'cache'
# COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
# COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_CSS_FILTERS = ["compressor.filters.yuglify.YUglifyCSSFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.yuglify.YUglifyJSFilter"]

# App Constants
# Project related
APP_CONSTANT_COMPANY = 'acgroup'
APP_CONSTANT_APP_NAME = "ACG-INCITY-APIS"
APP_CONSTANT_APP_SHORT_NAME = "ACG-INCITY-APIS"
APP_CONSTANT_APP_NAME_NO_SPACE = "ACG-INCITY-APIS"
APP_CONSTANT_APP_PACKAGE_NAME = "acgroup-incity-apis"
APP_CONSTANT_APP_VERSION_CODE = "v1.0.0"
APP_CONSTANT_APP_VERSION_NAME = "v1.0.0"
APP_CONSTANT_APP_VERSION_MOBILE = "v1 (1.0.0)"
APP_CONSTANT_COMPANY_NAME = "AC Group Ltd."
APP_CONSTANT_COMPANY_WEBSITE = "https://acgroup.rw"
APP_CONSTANT_TECH_SUPPORT_EMAIL_ID = "support@acgroup.rw"
APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID = APP_CONSTANT_TECH_SUPPORT_EMAIL_ID

# AC Group - NIDA Details
ACG_NIDA_URL = 'https://onlineauthentication.nida.gov.rw/onlineauthentication'
ACG_NIDA_PORT = "443"
ACG_NIDA_USERNAME = 'ACGroup'
ACG_NIDA_PASSWORD = '!gC$ztiO51yd3AmCA0TMLm1K0e?4Xc1f$y@txiqXcbj5TnSZj@a-nthYv8nvvu63ashFF8esK$JJc$7OCpU1c18Tqn?F@@BYkx5Benus7ZGr0PWzaQ8gQe0qAEps!PwP'
ACG_NIDA_KEYPHRASE = '8dU@h1NUY3bJwuYO67NGAMOzBizF0i?QJ7m?Vn5iJV_WD?HbW3mZH6CxFvL_Ch9P6CaEh09TbE_VN7$DSyZ??ohTF5HzT6XA1z6a?c9@9KXd7X0Ozgxdz$SSvy_stK-m'
ACG_NIDA_API_CLAIM_TOKEN = ACG_NIDA_URL+'/claimtoken'
ACG_NIDA_API_GET_CITIZEN = ACG_NIDA_URL+'/getcitizen'
ACG_NIDA_API_GET_ALL_MSIDNS = ACG_NIDA_URL + '/GetAllMSIDNs'

# NIDA Details
API_URL = ''
API_URL_BY_PHONE = 'https://nida.qtsoftwareltd.com:8080/api/v1/get-details/2/'
API_TOKEN = 'f3d99118-dd23-42d9-894e-d8cfef07bfd8'

# Email Settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # 587,465
EMAIL_HOST_USER = 'demo.techcible@gmail.com'
EMAIL_HOST_PASSWORD = 'Kigali@123'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Email Verification
EMAIL_VERIFICATION_SUBJECT = APP_CONSTANT_APP_NAME_NO_SPACE + " : Email Verification"
EMAIL_VERIFICATION_MESSAGE = "Thank you for registration. An email has been sent for verification."
EMAIL_VERIFICATION_MESSAGE_SUCCESS = "Your email id has been verified successfully. Please login to continue."
EMAIL_VERIFICATION_MESSAGE_WARNING = "Failed to verify your email id!"
EMAIL_VERIFICATION_MESSAGE_ERROR = "Verification Link is not valid!!!"
# Email Reset Password
EMAIL_PASSWORD_RESET_SUBJECT = APP_CONSTANT_APP_NAME_NO_SPACE + " : Reset Password"
EMAIL_PASSWORD_RESET_MESSAGE = "A link has been sent to your registered Email ID to reset your password."
# Email Message
EMAIL_NOTIFICATION_SUBJECT = APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
EMAIL_NOTIFICATION_MESSAGE = "Message"

# Google Recptcha
RECAPTCHA_PUBLIC_KEY = '6LfEo8UUAAAAAC2sfEG2Xcv5aQNceAB9QzfdHHtU'
GOOGLE_RECAPTCHA_SECRET_KEY = RECAPTCHA_PRIVATE_KEY = '6LfEo8UUAAAAAKu9QvLVb4wH4aFwObPxDMeJkEKs'
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True

# General
ERROR_MESSAGE = "Oops! Something went wrong. Please contact admin for support."
MAX_LOGIN_ATTEMPTS_CAPTCHA = 3

# # cors
# CORS_ORIGIN_WHITELIST = (
#     'localhost:8000',
#     '127.0.0.1:8000'
# )

# External Library Constants
# User Agent
# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

# Backend Sections
BACKEND_SECTION_DASHBOARD = 1
BACKEND_SECTION_OPERATORS = 2
BACKEND_SECTION_PROFILE = 3
BACKEND_SECTION_CHANGE_PASSWORD = 4
BACKEND_SECTION_SETTINGS = 5
BACKEND_SECTION_HELP = 6
BACKEND_SECTION_ORGANIZATIONS = 7
BACKEND_SECTION_LOGS = 8

# Access Permissions
ACCESS_PERMISSION_OPERATOR_CREATE = 'operator-create'
ACCESS_PERMISSION_OPERATOR_UPDATE = 'operator-update'
ACCESS_PERMISSION_OPERATOR_DELETE = 'operator-delete'
ACCESS_PERMISSION_OPERATOR_VIEW = 'operator-view'
ACCESS_PERMISSION_DASHBOARD_VIEW = 'dashboard-view'
ACCESS_PERMISSION_SETTINGS_VIEW = 'settings-view'
ACCESS_PERMISSION_LOG_CREATE = 'log-create'
ACCESS_PERMISSION_LOG_UPDATE = 'log-update'
ACCESS_PERMISSION_LOG_DELETE = 'log-delete'
ACCESS_PERMISSION_LOG_VIEW = 'log-view'
ACCESS_PERMISSION_ORGANIZATION_CREATE = 'organization-create'
ACCESS_PERMISSION_ORGANIZATION_UPDATE = 'organization-update'
ACCESS_PERMISSION_ORGANIZATION_DELETE = 'organization-delete'
ACCESS_PERMISSION_ORGANIZATION_VIEW = 'organization-view'

# Model Titles
MODEL_OPERATORS_PLURAL_TITLE = 'Operators'
MODEL_OPERATORS_SINGULAR_TITLE = 'Operator'
MODEL_ORGANIZATIONS_PLURAL_TITLE = 'Organizations'
MODEL_ORGANIZATIONS_SINGULAR_TITLE = 'Organization'
MODEL_CARDS_LOGS_PLURAL_TITLE = 'Card Logs'
MODEL_CARDS_LOGS_SINGULAR_TITLE = 'Card Log'

# Status Colors
STATUS_ACTIVE_COLOR = '#2ECC71'
STATUS_INACTIVE_COLOR = '#7F8C8D'
STATUS_BLOCKED_COLOR = '#E74C3C'
STATUS_UNVERIFIED_COLOR = '#2980B9'
STATUS_UNAPPROVED_COLOR = '#FFC300'

# Image Extensions
MAX_IMAGE_UPLOAD_SIZE = 4 * 1024 * 1024  # 4MB
VALID_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']
VALID_IMAGE_MIMES = ("image/png", "image/jpeg")

# File Extensions
MAX_FILE_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
VALID_FILE_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
VALID_FILE_MIMES = ("image/png", "image/jpeg")

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(asctime)s %(message)s'
#         },
#     },
#     'handlers': {
#         'db_log': {
#             'level': 'DEBUG',
#             'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
#         },
#     },
#     'loggers': {
#         'db': {
#             'handlers': ['db_log'],
#             'level': 'DEBUG'
#         }
#     }
# }

TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# Template Colors
COLOR_PRIMARY = '#1976d2'
COLOR_PRIMARY_DARK = '#1976d2'
COLOR_PRIMARY_LIGHT = '#1976d2'
COLOR_ACCENT = '#D21976'
