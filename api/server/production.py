import os

# Disable debug
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = [".api.beta.atados.com.br"]

# Secret key
# SECRET_KEY=False

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
