from django.test import TestCase
from django.utils import timezone

from ovp.apps.organizations.models import Organization
from ovp.apps.users.models import User
from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Apply
from ovp.apps.projects.models import Job
from ovp.apps.ratings.models import RatingRequest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

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

  def test_organization_score(self):
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")
    self.assertEqual(RatingRequest.objects.all().count(), 0)
    self.project.closed = True
    self.project.save()
    self.assertEqual(RatingRequest.objects.all().count(), 4)

    data = {
      "answers": [
        {
          "parameter_slug": "project-score",
          "value_quantitative": 1
        },
        {
          "parameter_slug": "project-how-was-it",
          "value_qualitative": "Minha resposta :-)"
        }
      ]
    }
    uuid = str(RatingRequest.objects.filter(requested_user=self.user)[1].uuid)
    client = APIClient()
    client.force_authenticate(user=self.user)
    response = client.post(reverse("rating-request-rate", [uuid]), data, format="json")
    self.assertEqual(response.status_code, 200)

    data["answers"][0]["value_quantitative"] = 0
    uuid = str(RatingRequest.objects.filter(requested_user=self.user)[3].uuid)
    response = client.post(reverse("rating-request-rate", [uuid]), data, format="json")
    self.assertEqual(response.status_code, 200)

    organization = Organization.objects.get(pk=self.organization.pk)
    self.assertEqual(organization.rating, 0.5)
    
  def test_user_score(self):
    Apply.objects.create(user=self.user, project=self.project, object_channel="default")
    self.assertEqual(RatingRequest.objects.all().count(), 0)
    self.project.closed = True
    self.project.save()
    self.assertEqual(RatingRequest.objects.all().count(), 4)

    data = {
      "answers": [
        {
          "parameter_slug": "volunteer-score",
          "value_quantitative": 1
        }
      ]
    }
    uuid = str(RatingRequest.objects.filter(requested_user=self.user)[0].uuid)
    client = APIClient()
    client.force_authenticate(user=self.user)
    response = client.post(reverse("rating-request-rate", [uuid]), data, format="json")
    self.assertEqual(response.status_code, 200)

    data["answers"][0]["value_quantitative"] = 0
    uuid = str(RatingRequest.objects.filter(requested_user=self.user)[2].uuid)
    response = client.post(reverse("rating-request-rate", [uuid]), data, format="json")
    self.assertEqual(response.status_code, 200)

    user = User.objects.get(pk=self.user.pk)
    self.assertEqual(user.rating, 0.5)