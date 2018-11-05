from django.test import TestCase
from django.utils import timezone

from ovp.apps.organizations.models import Organization
from ovp.apps.users.models import User
from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Apply
from ovp.apps.projects.models import Job
from ovp.apps.ratings.models import RatingRequest

class RatingRequestSignals(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(name="a", email="testmail-projects@test.com", password="test_returned", object_channel="default")
    self.organization = Organization.objects.create(name="test org", owner=self.user, object_channel="default")
    self.project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, organization=self.organization, published=False, object_channel="default")
    self.project2 = Project.objects.create(name="test project2", slug="test-slug", details="abc", description="abc", owner=self.user, organization=self.organization, published=False, object_channel="default")
    Job.objects.create(project=self.project, start_date=timezone.now(), end_date=timezone.now(), object_channel="default")
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")
    Apply.objects.create(user=self.user, project=self.project2, object_channel="default")

  def test_project_closing_creates_rating_request(self):
    self.assertEqual(RatingRequest.objects.all().count(), 0)
    self.project.closed = True
    self.project.save()
    self.assertEqual(RatingRequest.objects.all().count(), 2)
    self.assertEqual(RatingRequest.objects.first().rating_parameters.count(), 1)
    self.assertEqual(RatingRequest.objects.last().rating_parameters.count(), 2)

    self.project2.closed = True
    self.project2.save()
    self.assertEqual(RatingRequest.objects.all().count(), 2)