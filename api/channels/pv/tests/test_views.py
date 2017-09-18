from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from channels.pv import models

@override_settings(DEFAULT_SEND_EMAIL="sync")
class MeetingViewSetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

  def test_list_meeting_dates(self):
    """ Test list route. Assert only upcoming meetings are shown """
    response = self.client.get(reverse("meeting-list"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(len(response.data), 0)

    models.PVMeetingDate.objects.create(date=timezone.now(), object_channel="pv")
    models.PVMeetingDate.objects.create(date=timezone.now()+timedelta(hours=1), object_channel="pv")

    response = self.client.get(reverse("meeting-list"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(len(response.data), 1)
    self.assertTrue("date" in response.data[0])
    self.assertTrue("id" in response.data[0])
