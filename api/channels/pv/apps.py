from django.apps import AppConfig

class PvConfig(AppConfig):
  name = 'channels.pv'

  def ready(self):
    from . import signals
