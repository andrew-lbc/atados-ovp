from channels.pv.models import PVMeeting

from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers

class MeetingSerializer(ChannelRelationshipSerializer):
  date = serializers.DateTimeField()

  class Meta:
    model = PVMeeting
    fields = ["id", "date"]
