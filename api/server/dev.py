from corsheaders.defaults import default_headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
  'x-unauthenticated-upload',
  'x-ovp-channel'
)
INTERNAL_IPS = ('127.0.0.1', )
ALLOWED_HOSTS = ['.localhost', '.local.atados.com.br']

# Email
EMAIL_HOST='smtp.mailtrap.io'
EMAIL_PORT=2525
EMAIL_HOST_USER='6de59c7765835e'
EMAIL_HOST_PASSWORD='54799aa8d94886'

# Haystack
HAYSTACK_SIGNAL_PROCESSOR='ovp.apps.search.signals.TiedModelRealtimeSignalProcessor'