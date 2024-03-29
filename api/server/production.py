import os
import dj_database_url

# Base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Disable debug
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = ['api.beta.atados.com.br', '.admin.beta.atados.com.br', 'v2.api.atados.com.br', '.admin.atados.com.br', '.admin.voluntariadotransforma.com.br', '.admin.rederealpanorama.com.br']

# Cors
CORS_ORIGIN_WHITELIST = [
  'http://localhost:8080',
  'http://integrinodejs.mybluemix.net',
  'https://integrinodejs.mybluemix.net',
  'https://atados.com.br',
  'https://integri.org',
  'https://www.atados.com.br',
  'https://beta.atados.com.br',
  'http://localhost:3000',
  'https://voluntariadotransforma.com.br',
  'http://voluntariadotransforma.com.br',
  'https://rederealpanorama.com.br',
]

# Secret key
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Email
EMAIL_BACKEND = 'email_log.backends.EmailBackend'

# Media and static files
MEDIA_ROOT= '/tmp'

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'ovp.apps.search.backends.ConfigurableElasticSearchEngine',
    'URL': 'http://%s/' % (os.environ.get('HS_SEARCH_ENDPOINT', '127.0.0.1:9200')),
    'INDEX_NAME': 'atadosovp'
  },
}

# Logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse',
    }
  },
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': '/home/ubuntu/api/logs/django.log',
    },
    'rollbar': {
      'filters': ['require_debug_false'],
      'access_token': os.environ.get('ROLLBAR_SERVER_TOKEN'),
      'environment': 'production',
      'class': 'rollbar.logger.RollbarHandler',
    },
  },
  'loggers': {
    'django': {
      'handlers': ['file', 'rollbar'],
      'level': 'DEBUG',
      'propagate': True,
    },
  },
}


# Storage
DEFAULT_FILE_STORAGE = 'django_gcloud_storage.DjangoGCloudStorage'
GCS_PROJECT = 'beta-atados'
GCS_CREDENTIALS_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../../', 'storage.json'))
GCS_USE_UNSIGNED_URLS = True
GCS_BUCKET = 'atados-v3'

# Database
DATABASES = {
  'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}

# Rollbar

ROLLBAR = {
  'access_token': os.environ.get('ROLLBAR_SERVER_TOKEN'),
  'environment': 'production',
  'branch': 'master',
  'root': BASE_DIR,
}
