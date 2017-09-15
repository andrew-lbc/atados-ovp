from django.db import models

class PVUserInfo(models.Model):
  can_apply = models.BooleanField(default=False)
