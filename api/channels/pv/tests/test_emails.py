from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.core import mail

from ovp.apps.core.helpers import get_email_subject
from ovp.apps.users.models import User

from channels.pv.models import PVMeeting
from channels.pv.models import PVMeetingAppointment

from server.celery import app

@override_settings(DEFAULT_SEND_EMAIL="sync")
class TestEmailTriggers(TestCase):
  def setUp(self):
    self.meeting = PVMeeting.objects.create(date=timezone.now()+timedelta(days=2), object_channel="pv")
    self.user = User.objects.create(email="test_user", password="testpw", object_channel="pv")
    app.control.purge()

  def test_appointment_trigger_email(self):
    """Assert that email is triggered when creating an appointment """
    mail.outbox = []

    PVMeetingAppointment.objects.create(user=self.user, meeting=self.meeting, object_channel="pv")

    self.assertTrue(len(mail.outbox) == 1)
    self.assertTrue(mail.outbox[0].subject == get_email_subject("pv", "appointmentCreated", "Appointment created"))
