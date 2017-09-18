from rest_framework import routers
from django.conf.urls import url, include
from channels.pv.views import MeetingViewSet

router = routers.SimpleRouter()
router.register(r'meetings', MeetingViewSet, 'meeting')

urlpatterns = [
  url(r'^', include(router.urls)),
]
