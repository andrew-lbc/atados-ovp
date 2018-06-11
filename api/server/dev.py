from corsheaders.defaults import default_headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
  'x-unauthenticated-upload',
  'x-ovp-channel'
)
INTERNAL_IPS = ('127.0.0.1', )
ALLOWED_HOSTS = ['.localhost', '.local.atados.com.br']
