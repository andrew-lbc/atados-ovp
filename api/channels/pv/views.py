from django.utils import timezone

from channels.pv import models
from channels.pv import serializers

from ovp.apps.channels.viewsets.decorators import ChannelViewSet
from ovp.apps.core import pagination

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets

@ChannelViewSet
class MeetingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  Meetings viewpoints.

  View available dates e create an appointment.
  """
  queryset = models.PVMeeting.objects.all()
  pagination_class = pagination.NoPagination

  @decorators.detail_route(["POST"])
  def appoint(self, request, *args, **kwargs):
    meeting = self.get_object()
    try:
      models.PVMeetingAppointment.objects.get(user=request.user, meeting=meeting, channel__slug=request.channel)
      return response.Response({"detail": "Can\'t appoint to this meeting because you are already appointed."}, status=status.HTTP_400_BAD_REQUEST)
    except models.PVMeetingAppointment.DoesNotExist:
      models.PVMeetingAppointment.objects.create(user=request.user, meeting=meeting, object_channel=request.channel)
      return response.Response({"detail": "Successfully appointed."}, status=status.HTTP_200_OK)

  @decorators.detail_route(["POST"])
  def unappoint(self, request, *args, **kwargs):
    meeting = self.get_object()
    try:
      appointment = models.PVMeetingAppointment.objects.get(user=request.user, meeting=meeting, channel__slug=request.channel)
      appointment.delete()
      return response.Response({"detail": "Successfully unappointed."}, status=status.HTTP_200_OK)
    except models.PVMeetingAppointment.DoesNotExist:
      return response.Response({"detail": "Can\'t unappoint to this meeting because you are not appointed."}, status=status.HTTP_400_BAD_REQUEST)

  @decorators.list_route(["GET"])
  def appointments(self, request, *args, **kwargs):
    appointments = self.get_queryset().filter(pvmeetingappointment__user=request.user, channel__slug=request.channel)
    serializer = self.get_serializer(appointments, many=True, context=self.get_serializer_context())
    return response.Response(serializer.data, status=status.HTTP_200_OK)


  """
  Meta
  """
  def get_queryset(self):
    if self.action in ["list", "appoint", "unappoint"]:
      return self.queryset.filter(date__gte=timezone.now())
    if self.action == "appointments":
      return self.queryset

  def get_serializer_class(self):
    request = self.get_serializer_context()["request"]

    if self.action in ["list", "appointments"]:
      return serializers.MeetingSerializer

  def get_permissions(self):
    request = self.get_serializer_context()["request"]

    if self.action == "list":
      self.permission_classes = ()

    if self.action in ["appoint", "unappoint", "appointments"]:
      self.permission_classes = (permissions.IsAuthenticated, )

    return super(MeetingViewSet, self).get_permissions()
