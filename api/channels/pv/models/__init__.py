from django.db import models
from channels.pv import emails
from ovp.apps.channels.models.abstract import ChannelRelationship

class PVUserInfo(ChannelRelationship):
  user = models.OneToOneField("users.User")
  can_apply = models.BooleanField(default=False)

  def __init__(self, *args, **kwargs):
    super(PVUserInfo, self).__init__(*args, **kwargs)
    self.__original_can_apply = self.can_apply

  def mailing(self, async_mail=None):
    return emails.UserInfoMail(self, async_mail)

  def save(self, *args, **kwargs):
    send_email = False
    if self.can_apply != self.__original_can_apply:
      send_email = True

    super(PVUserInfo, self).save(*args, **kwargs)
    self.__original_can_apply = self.can_apply

    if send_email:
      self.mailing().sendApproved()

class PVMeeting(ChannelRelationship):
  date = models.DateTimeField()
  published = models.BooleanField(default=True)
  address = models.OneToOneField('core.GoogleAddress', blank=True, null=True, verbose_name='address', db_constraint=False)
  max_appointments = models.IntegerField(default=40)

class PVMeetingAppointment(ChannelRelationship):
  meeting = models.ForeignKey("PVMeeting", related_name="appointments")
  user = models.ForeignKey("users.User")

  def can_apply(self):
    return self.user.pvuserinfo.can_apply
  can_apply.boolean = True

  def mailing(self, async_mail=None):
    return emails.AppointmentMail(self, async_mail)

  def save(self, *args, **kwargs):
    creating = False
    if not self.pk:
      creating = True

    super(PVMeetingAppointment, self).save(*args, **kwargs)

    if creating:
      self.mailing().sendCreated({"appointment": self})
