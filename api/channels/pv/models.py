from django.db import models
from ovp.apps.channels.models.abstract import ChannelRelationship

class PVUserInfo(ChannelRelationship):
  user = models.OneToOneField("users.User")
  can_apply = models.BooleanField(default=False)

class PVMeetingDate(ChannelRelationship):
  date = models.DateTimeField()

class PVMeetingAppointment(ChannelRelationship):
  meeting_date = models.ForeignKey('PVMeetingDate')
  user = models.ForeignKey("users.User")
