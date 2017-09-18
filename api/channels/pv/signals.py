from django.db.models.signals import post_save

from channels.pv.models import PVUserInfo

from ovp.apps.projects.views.apply import ApplyResourceViewSet

from ovp.apps.channels.signals import before_channel_request
from ovp.apps.channels.exceptions import InterceptRequest

from ovp.apps.users.models import User

from rest_framework import response

def intercept_apply(sender, *args, **kwargs):
  """
  Block requests to apply route if user cannot apply
  """
  request = kwargs["request"]
  if request.method.lower() == "post" and request.channel == "pv":
    if request.user.is_authenticated() and not request.user.pvuserinfo.can_apply:
      raise InterceptRequest(response.Response({'detail': 'You are not yet authorized to apply. You have to participate in a meeting or respond the quiz first.'}, status=403))

def create_pv_profile(sender, *args, **kwargs):
  """
  Create PVUserInfo after user is created on pv channel
  """
  instance = kwargs["instance"]
  if instance.channel.slug == "pv" and kwargs["created"] and not kwargs["raw"]:
    PVUserInfo.objects.create(user=instance, object_channel="pv")

before_channel_request.connect(intercept_apply, sender=ApplyResourceViewSet)
post_save.connect(create_pv_profile, sender=User)
