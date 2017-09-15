from django.test import TestCase
from django.test.utils import override_settings

from channels.pv.models import PVUserInfo

from ovp.apps.users.models import User

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

@override_settings(DEFAULT_SEND_EMAIL="sync")
class ApplySignalTestCase(TestCase):
  def setUp(self):
    #user = User.objects.create(email="test@email.com", password="test_password", object_channel="pv")
    self.client = APIClient()

  def test_pvinfo_is_created_when_user_is_created(self):
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
