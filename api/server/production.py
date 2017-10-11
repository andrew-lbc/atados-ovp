DEBUG = False
#SECRET_KEY=False
EMAIL_BACKEND = 'email_log.backends.EmailBackend'
MEDIA_ROOT= '/tmp'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_SECURE_URLS = True
AWS_S3_URL_PROTOCOL = 'https'
AWS_HEADERS = {
    'Expires': 'Sat, 31 Dec 2016 23:59:59 GMT'
}

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
    'URL': 'http://%s/' % (os.environ.get('HS_SEARCH_ENDPOINT', '127.0.0.1:9200')),
    'INDEX_NAME': 'atadosovp'
  },
}

# Logging
