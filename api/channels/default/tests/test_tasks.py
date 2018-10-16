from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.core import mail

from ovp.apps.core.helpers import get_email_subject
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Apply
from ovp.apps.projects.models import Job
from ovp.apps.projects.models import Work

from server.celery import app

@override_settings(DEFAULT_SEND_EMAIL="sync",
                    CELERY_TASK_EAGER_PROPAGATES_EXCEPTIONS=True,
                    CELERY_TASK_ALWAYS_EAGER=True)
class TestEmailTriggers(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(name="a", email="testmail-projects@test.com", password="test_returned", object_channel="default")
    self.organization = Organization.objects.create(name="test org", owner=self.user, object_channel="default")
    self.project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, organization=self.organization, published=False, object_channel="default")
    self.project.published = True
    self.project.save()

    app.control.purge()

  def test_applying_schedules_interaction_confirmation_email(self):
    """Assert cellery task to ask about interaction is created when user applies to project"""
    mail.outbox = []
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")

    self.assertTrue(len(mail.outbox) == 2)
    self.assertTrue(mail.outbox[0].subject == get_email_subject("default", "atados-askProjectInteractionConfirmation-toVolunteer", "Ask project confirmation"))
    self.assertTrue("vaga test project" in mail.outbox[0].body)

  def test_applying_schedules_reminder_email(self):
    """Assert cellery task to remind volunteer is created when user applies to project"""
    mail.outbox = []
    Job.objects.create(project=self.project, start_date=timezone.now(), end_date=timezone.now(), object_channel="default")
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")

    self.assertTrue(len(mail.outbox) == 4)
    self.assertTrue(mail.outbox[1].subject == "Uma ação está chegando... estamos ansiosos para te ver.")
    self.assertTrue("test project" in mail.outbox[1].body)

  def test_applying_schedules_ask_about_project_experience_to_volunteer(self):
    """Assert cellery task to ask volunteer about project experience is created when user applies to project"""
    mail.outbox = []
    work = Work.objects.create(project=self.project, object_channel="default")
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")

    self.assertTrue(len(mail.outbox) == 3)
    self.assertTrue(mail.outbox[1].subject == "Conta pra gente como foi sua experiência?")
    self.assertTrue(">test project<" in mail.outbox[1].alternatives[0][0])

    mail.outbox = []
    work.delete()
    job = Job.objects.create(project=self.project, start_date=timezone.now(), end_date=timezone.now(), object_channel="default")
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")

    self.assertTrue(mail.outbox[2].subject == "Conta pra gente como foi sua experiência?")
    self.assertTrue(">test project<" in mail.outbox[2].alternatives[0][0])

  def test_publishing_project_schedules_ask_about_experience_to_organization(self):
    """Assert cellery task to ask organization about project experience is created when user project is published"""
    mail.outbox = []

    project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, published=False, organization=self.organization, object_channel="default")
    work = Work.objects.create(project=project, object_channel="default")
    project.published = True
    project.save()

    self.assertTrue(len(mail.outbox) == 3)
    self.assertTrue(mail.outbox[2].subject == "Tá na hora de contar pra gente como foi")
    self.assertTrue(">test project<" in mail.outbox[2].alternatives[0][0])