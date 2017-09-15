from ovp.apps.channels.signals import before_channel_request

def before_request(sender, *args, **kwargs):
  print(kwargs)
  print("KEKE")
before_channel_request.connect(before_request)
