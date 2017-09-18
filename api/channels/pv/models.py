from django.db import models
from ovp.apps.channels.models.abstract import ChannelRelationship

class PVUserInfo(ChannelRelationship):
  user = models.OneToOneField("users.User")
  can_apply = models.BooleanField(default=False)

class PVMeeting(ChannelRelationship):
  date = models.DateTimeField()

class PVMeetingAppointment(ChannelRelationship):
  meeting = models.ForeignKey("PVMeeting")
  user = models.ForeignKey("users.User")
