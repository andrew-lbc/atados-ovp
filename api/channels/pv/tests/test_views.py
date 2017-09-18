from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.users.models import User

from channels.pv import models

@override_settings(DEFAULT_SEND_EMAIL="sync")
class MeetingViewSetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()
    models.PVMeeting.objects.create(date=timezone.now(), object_channel="pv")
    models.PVMeeting.objects.create(date=timezone.now()+timedelta(hours=1), object_channel="pv")

    self.user = User.objects.create(email="test_user", password="testpw", object_channel="pv")

  def test_list_meeting_dates(self):
    """ Test list route. Assert only upcoming meetings are shown. """
    models.PVMeeting.objects.all().delete()
    response = self.client.get(reverse("meeting-list"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(len(response.data), 0)

    models.PVMeeting.objects.create(date=timezone.now(), object_channel="pv")
    models.PVMeeting.objects.create(date=timezone.now()+timedelta(hours=1), object_channel="pv")

    response = self.client.get(reverse("meeting-list"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(len(response.data), 1)
    self.assertTrue("date" in response.data[0])
    self.assertTrue("id" in response.data[0])

  def test_can_appoint(self):
    pk = models.PVMeeting.objects.last().pk
    self.client.logout()
    response = self.client.post(reverse("meeting-appoint", [pk]), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 401)

    self.client.force_authenticate(user=self.user)
    response = self.client.post(reverse("meeting-appoint", [pk]), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, {"detail": "Successfully appointed."})

  def test_can_unappoint(self):
    pk = models.PVMeeting.objects.last().pk
    response = self.client.post(reverse("meeting-unappoint", [pk]), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 401)

    self.assertEqual(models.PVMeetingAppointment.objects.filter(user=self.user, meeting__pk=pk, channel__slug="pv").count(), 0)
    self.test_can_appoint()
    self.assertEqual(models.PVMeetingAppointment.objects.filter(user=self.user, meeting__pk=pk, channel__slug="pv").count(), 1)

    self.client.force_authenticate(user=self.user)
    response = self.client.post(reverse("meeting-unappoint", [pk]), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, {"detail": "Successfully unappointed."})

    self.assertEqual(models.PVMeetingAppointment.objects.filter(user=self.user, meeting__pk=pk, channel__slug="pv").count(), 0)
    response = self.client.post(reverse("meeting-unappoint", [pk]), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.data, {"detail": "Can\'t unappoint to this meeting because you are not appointed."})

  def test_cant_appoint_twice_to_same_meeting(self):
    self.test_can_appoint()

    pk = models.PVMeeting.objects.last().pk
    response = self.client.post(reverse("meeting-appoint", [pk]), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.data, {"detail": "Can\'t appoint to this meeting because you are already appointed."})

  def test_can_retrieve_appointments(self):
    response = self.client.get(reverse("meeting-appointments"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 401)

    self.client.force_authenticate(user=self.user)
    response = self.client.get(reverse("meeting-appointments"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 0)

    self.test_can_appoint()
    response = self.client.get(reverse("meeting-appointments"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)
