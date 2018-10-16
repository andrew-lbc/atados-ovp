from django.utils import timezone

from channels.pv import models
from channels.pv import serializers

from ovp.apps.channels.viewsets.decorators import ChannelViewSet
from ovp.apps.core import pagination
from ovp.apps.users.models import User

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets

from drf_yasg.utils import swagger_auto_schema

@ChannelViewSet
class MeetingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  """
  Meetings viewpoints.

  View available dates e create an appointment.
  """
  queryset = models.PVMeeting.objects.all()
  pagination_class = pagination.NoPagination
  swagger_schema = None

  @decorators.action(methods=["POST"], detail=True)
  def appoint(self, request, *args, **kwargs):
    meeting = self.get_object()
    try:
      models.PVMeetingAppointment.objects.get(user=request.user, meeting=meeting, channel__slug=request.channel)
      return response.Response({"detail": "Can\'t appoint to this meeting because you are already appointed."}, status=status.HTTP_400_BAD_REQUEST)
    except models.PVMeetingAppointment.DoesNotExist:
      if meeting.appointments.count() >= meeting.max_appointments:
        return response.Response({"detail": "This meeting has exceeded the maximum amount of appointments."}, status=status.HTTP_400_BAD_REQUEST)
      else:
        models.PVMeetingAppointment.objects.create(user=request.user, meeting=meeting, object_channel=request.channel, special_conditions=request.data.get('special_conditions', None))
        return response.Response({"detail": "Successfully appointed."}, status=status.HTTP_200_OK)

  @decorators.action(methods=["POST"], detail=True)
  def unappoint(self, request, *args, **kwargs):
    meeting = self.get_object()
    try:
      appointment = models.PVMeetingAppointment.objects.get(user=request.user, meeting=meeting, channel__slug=request.channel)
      appointment.delete()
      return response.Response({"detail": "Successfully unappointed."}, status=status.HTTP_200_OK)
    except models.PVMeetingAppointment.DoesNotExist:
      return response.Response({"detail": "Can\'t unappoint to this meeting because you are not appointed."}, status=status.HTTP_400_BAD_REQUEST)

  @decorators.action(methods=["GET"], detail=False)
  def appointments(self, request, *args, **kwargs):
    appointments = self.get_queryset().filter(appointments__user=request.user, channel__slug=request.channel, published=True)
    serializer = self.get_serializer(appointments, many=True, context=self.get_serializer_context())
    return response.Response(serializer.data, status=status.HTTP_200_OK)


  """
  Meta
  """
  def get_queryset(self):
    if self.action in ["list", "appoint", "unappoint"]:
      return self.queryset.filter(date__gte=timezone.now(), published=True)
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


@ChannelViewSet
class QuizViewSet(viewsets.GenericViewSet):
  """
  Quiz viewpoints.

  This will be deprecated once OVP has forms functionality.
  """
  permission_classes = (permissions.IsAuthenticated, )
  swagger_schema = None

  @decorators.action(methods=["POST"], detail=False)
  def respond(self, request, *args, **kwargs):
    correct_answers = ["a", "c", "b", "a", "e"]
    threesold = 1

    answers = request.data.get("answers", [])
    if len(answers) != len(correct_answers):
      return response.Response({"title": "answers_incomplete", "detail": "Answer amount does not match questions amount."}, status=status.HTTP_400_BAD_REQUEST)

    matches = 0
    for i, answer in enumerate(answers):
      if answer == correct_answers[i]:
        matches += 1

    result = matches/len(answers)

    if result < threesold:
      return response.Response({"title": "answers_not_correct", "detail": "You did not meet the correct answers threesold."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.pvuserinfo.can_apply = True
    request.user.pvuserinfo.save()

    return response.Response({"detail": "You have passed the test."}, status=status.HTTP_200_OK)


@swagger_auto_schema(method="GET", auto_schema=None)
@decorators.api_view(["GET"])
def user_can_apply(request, *args, **kwargs):
  if request.user.pk is None:
    return response.Response({"detail": "Authentication credentials were not provided."}, status=400)

  user = User.objects.get(pk=request.user.pk)
  if user.pvuserinfo.can_apply:
    return response.Response({"status": True}, status=200)

  return response.Response({"status": False, "detail": "Current user cannot apply yet."}, status=400)


@swagger_auto_schema(method="POST", auto_schema=None)
@decorators.api_view(["POST"])
def virtual_meeting_trigger(request, *args, **kwargs):
  if request.user.pk is None:
    return response.Response({"detail": "Authentication credentials were not provided."}, status=400)

  user = User.objects.get(pk=request.user.pk)
  user.pvuserinfo.can_apply = True
  user.pvuserinfo.approved_by_virtual_meeting = True
  user.pvuserinfo.save()

  return response.Response({"status": True}, status=200)