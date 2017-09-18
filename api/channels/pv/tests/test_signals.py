from django.test import TestCase
from django.test.utils import override_settings

from channels.pv.models import PVUserInfo

from ovp.apps.users.models import User

from ovp.apps.projects.models import Project

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

@override_settings(DEFAULT_SEND_EMAIL="sync")
class ApplySignalTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

  def test_pvinfo_is_created_when_user_is_created(self):
    """ Assert users on PV channel get associated with PVUserInfo model """
    data = {
      'name': 'Valid Name',
      'email': 'test@email.com',
      'password': 'test@password.com'
    }

    # Creating user on PV creates PVUserInfo
    self.assertEqual(PVUserInfo.objects.count(), 0)
    response = self.client.post(reverse('user-list'), data, format="json", HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(PVUserInfo.objects.count(), 1)
    self.assertEqual(str(PVUserInfo.objects.first().user.uuid), response.data["uuid"])
    self.assertEqual(PVUserInfo.objects.first().can_apply, False)

    # Creating user on other channel does not create PVUserInfo
    response = self.client.post(reverse('user-list'), data, format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(PVUserInfo.objects.count(), 1)

  def test_pv_users_get_blocked_on_apply(self):
    """ Assert users on PV channel get blocked on apply if PVUserInfo.can_apply == False """
    self.test_pvinfo_is_created_when_user_is_created()
    user_pv = User.objects.get(channel__slug="pv")
    user_default = User.objects.get(channel__slug="default")
    project_pv = Project.objects.create(name="test project", details="abc", description="abc", owner=user_pv, object_channel="pv")
    project_default = Project.objects.create(name="test project", details="abc", description="abc", owner=user_pv, object_channel="default")

    self.client.force_authenticate(user=user_pv)
    response = self.client.post(reverse("project-applies-apply", ["test-project"]), format="json", HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.data, {'detail': 'You are not yet authorized to apply. You have to participate in a meeting or respond the quiz first.'})
    self.assertEqual(response.status_code, 403)

    user_pv.pvuserinfo.can_apply = True
    user_pv.pvuserinfo.save()

    self.client.force_authenticate(user=user_pv)
    response = self.client.post(reverse("project-applies-apply", ["test-project"]), format="json", HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 200)

    # Other channel users needn't permission to apply
    self.client.force_authenticate(user=user_default)
    response = self.client.post(reverse("project-applies-apply", ["test-project"]), format="json", HTTP_X_OVP_CHANNEL="default")
    self.assertEqual(response.status_code, 200)

@override_settings(DEFAULT_SEND_EMAIL="sync")
class BlockSignalTestCase(TestCase):
  def test_cant_request_pv_routes_from_other_channel(self):
    client = APIClient()
    response = client.get(reverse("meeting-list"), json=True)
    self.assertEqual(response.status_code, 400)

    response = client.get(reverse("meeting-list"), json=True, HTTP_X_OVP_CHANNEL="pv")
    self.assertEqual(response.status_code, 200)
