from channels.pv.models import PVMeetingDate

from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers

class MeetingDateSerializer(ChannelRelationshipSerializer):
  date = serializers.DateTimeField()

  class Meta:
    model = PVMeetingDate
    fields = ["id", "date"]
