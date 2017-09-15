from django.test import TestCase
from ovp.apps.users.models import User

# Create your tests here.
class ApplySignalTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(email="test@email.com", password="test_password", object_channel="pv")

  def test_signal_intercept_applies(self):
    pass
