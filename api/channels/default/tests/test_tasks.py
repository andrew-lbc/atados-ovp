from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.core import mail

from ovp.apps.core.helpers import get_email_subject
from ovp.apps.users.models import User
from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Apply

from server.celery import app

@override_settings(DEFAULT_SEND_EMAIL="sync",
                    CELERY_TASK_EAGER_PROPAGATES_EXCEPTIONS=True,
                    CELERY_TASK_ALWAYS_EAGER=True)
class TestEmailTriggers(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(name="a", email="testmail-projects@test.com", password="test_returned", object_channel="default")
    self.project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, published=True, object_channel="default")

    app.control.purge()

  def test_applying_sends_interaction_confirmation_email(self):
    """Assert cellery task is created when user applies to project"""
    mail.outbox = []
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")

    self.assertTrue(len(mail.outbox) == 2)
    self.assertTrue(mail.outbox[0].subject == get_email_subject("default", "atados-askProjectInteractionConfirmation-toVolunteer", "Ask project confirmation"))
    self.assertTrue("vaga test project" in mail.outbox[0].body)