from rest_framework import routers
from django.conf.urls import url, include
from channels.pv.views import MeetingViewSet
from channels.pv.views import QuizViewSet
from channels.pv.views import user_can_apply
from channels.pv.views import virtual_meeting_trigger

meetings = routers.SimpleRouter()
meetings.register(r'meetings', MeetingViewSet, 'meeting')

quiz = routers.SimpleRouter()
quiz.register(r'quiz', QuizViewSet, 'quiz')

urlpatterns = [
  url(r'^', include(meetings.urls)),
  url(r'^', include(quiz.urls)),
  url(r'^user-can-apply/', user_can_apply, name='user-can-apply'),
  url(r'^virtual-meeting-trigger/', virtual_meeting_trigger, name='virtual-meeting-trigger')
]
