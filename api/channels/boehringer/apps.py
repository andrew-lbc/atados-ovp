from django.apps import AppConfig

class BoehringerConfig(AppConfig):
  name = 'channels.boehringer'

  def ready(self):
    from . import content_flow
