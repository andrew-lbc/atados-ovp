from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.core import mail

from ovp.apps.core.helpers import get_email_subject
from ovp.apps.users.models import User

from channels.pv.models import PVMeeting
from channels.pv.models import PVMeetingAppointment
from channels.pv import tasks

from server.celery import app

@override_settings(DEFAULT_SEND_EMAIL="sync")
class TestEmailTriggers(TestCase):
  def setUp(self):
    self.meeting = PVMeeting.objects.create(date=timezone.now()+timedelta(days=2), object_channel="pv")
    self.user = User.objects.create(email="test_user", password="testpw", object_channel="pv")
    app.control.purge()

  @override_settings(DEFAULT_SEND_EMAIL="sync",
                     CELERY_TASK_EAGER_PROPAGATES_EXCEPTIONS=True,
                     CELERY_TASK_ALWAYS_EAGER=True)
  def test_appointment_notification_task(self):
    """Assert cellery task is created when creating an appointment """
    mail.outbox = []
    PVMeetingAppointment.objects.create(user=self.user, meeting=self.meeting, object_channel="pv")

    self.assertTrue(len(mail.outbox) == 2)
    self.assertTrue(mail.outbox[0].subject == get_email_subject("pv", "appointmentNotification", "Appointment notification"))