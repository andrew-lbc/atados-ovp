from django.apps import AppConfig

class RRPConfig(AppConfig):
  name = 'channels.rrp'

  def ready(self):
    from . import content_flow
