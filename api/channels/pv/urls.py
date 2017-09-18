from rest_framework import routers
from django.conf.urls import url, include
from channels.pv.views import MeetingViewSet
from channels.pv.views import QuizViewSet

meetings = routers.SimpleRouter()
meetings.register(r'meetings', MeetingViewSet, 'meeting')

quiz = routers.SimpleRouter()
quiz.register(r'quiz', QuizViewSet, 'quiz')

urlpatterns = [
  url(r'^', include(meetings.urls)),
  url(r'^', include(quiz.urls)),
]
