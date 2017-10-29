from channels.pv.models import PVMeeting

from ovp.apps.core.serializers import GoogleAddressSerializer
from ovp.apps.channels.serializers import ChannelRelationshipSerializer

from rest_framework import serializers

class MeetingSerializer(ChannelRelationshipSerializer):
  date = serializers.DateTimeField()
  address = GoogleAddressSerializer()
  appointments_count = serializers.SerializerMethodField()

  class Meta:
    model = PVMeeting
    fields = ["id", "date", "address", "max_appointments", "appointments_count"]

  def get_appointments_count(self, obj):
    return obj.appointments.count()
