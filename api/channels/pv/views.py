from django.utils import timezone

from channels.pv import models
from channels.pv import serializers

from ovp.apps.channels.viewsets.decorators import ChannelViewSet
from ovp.apps.core import pagination

from rest_framework import mixins
from rest_framework import viewsets

@ChannelViewSet
class MeetingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  Meetings viewpoints.

  View available dates e create an appointment.
  """
  queryset = models.PVMeetingDate.objects.all()
  pagination_class = pagination.NoPagination

  def get_queryset(self):
    if self.action == 'list':
      return self.queryset.filter(date__gte=timezone.now())

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']

    if self.action == 'list':
      return serializers.MeetingDateSerializer
