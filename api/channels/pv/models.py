from django.db import models

class PVUserInfo(models.Model):
  user = models.OneToOneField("users.User")
  can_apply = models.BooleanField(default=False)
