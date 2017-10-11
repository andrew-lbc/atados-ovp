import os

# Base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Disable debug
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['.api.beta.atados.com.br']

# Secret key
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Email
EMAIL_BACKEND = 'email_log.backends.EmailBackend'

# Media and static files
MEDIA_ROOT= '/tmp'

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    'URL': 'http://%s/' % (os.environ.get('HS_SEARCH_ENDPOINT', '127.0.0.1:9200')),
    'INDEX_NAME': 'atadosovp'
  },
}

# Logging
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': '/home/ubuntu/api/logs/django.log',
    },
  },
  'loggers': {
    'django': {
      'handlers': ['file'],
      'level': 'DEBUG',
      'propagate': True,

    },
  },
}


# Storage
DEFAULT_FILE_STORAGE = 'django_gcloud_storage.DjangoGCloudStorage'
GCS_PROJECT = 'atados-v3'
GCS_CREDENTIALS_FILE_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../../', 'storage.json'))
GCS_USE_UNSIGNED_URLS = True
