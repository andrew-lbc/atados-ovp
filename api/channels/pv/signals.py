from channels.pv.models import PVUserInfo

from ovp.apps.channels.signals import before_channel_request
from ovp.apps.channels.signals import after_channel_request

from ovp.apps.users.models import User
from ovp.apps.users.views import UserResourceViewSet

def intercept_apply(sender, *args, **kwargs):
  pass
before_channel_request.connect(intercept_apply)

def create_pv_profile(sender, *args, **kwargs):
  request = kwargs["request"]
  response = kwargs["response"]
  if request.channel == "pv":
    if request.method.lower() == "post" and response.status_code == 201:
      user = User.objects.get(uuid=response.data["uuid"])
      PVUserInfo.objects.create(user=user)

after_channel_request.connect(create_pv_profile, sender=UserResourceViewSet)

