from django.db import models
from django.utils.translation import ugettext_lazy as _
from channels.pv import emails
from ovp.apps.channels.models.abstract import ChannelRelationship

class PVUserInfo(ChannelRelationship):
  user = models.OneToOneField("users.User", verbose_name=_("user"))
  can_apply = models.BooleanField(_("Can Apply"), default=False)
  approved_by_virtual_meeting = models.BooleanField(_("Approved by virtual meeting"), default=False)

  def __init__(self, *args, **kwargs):
    super(PVUserInfo, self).__init__(*args, **kwargs)
    self.__original_can_apply = self.can_apply

  def mailing(self, async_mail=None):
    return emails.UserInfoMail(self, async_mail)

  def save(self, *args, **kwargs):
    send_email = False
    if self.can_apply and self.can_apply != self.__original_can_apply:
      send_email = True

    super(PVUserInfo, self).save(*args, **kwargs)
    self.__original_can_apply = self.can_apply

    if send_email:
      self.mailing().sendApproved()

  class Meta:
    app_label = "pv"
    verbose_name = _("PV User Info")
    verbose_name_plural = _("PV Users Info")

class PVMeeting(ChannelRelationship):
  date = models.DateTimeField(_("Date"))
  published = models.BooleanField(_("Published"), default=True)
  address = models.ForeignKey("core.GoogleAddress", blank=True, null=True, verbose_name=_("address"), db_constraint=False)
  max_appointments = models.IntegerField(_("Maximum appointments"), default=40)

  class Meta:
    app_label = "pv"
    verbose_name = _("PV Meeting")
    verbose_name_plural = _("PV Meetings")

class PVMeetingAppointment(ChannelRelationship):
  meeting = models.ForeignKey("PVMeeting", related_name="appointments", verbose_name=_("meeting"))
  user = models.ForeignKey("users.User", verbose_name=_("user"))
  special_conditions = models.CharField(_('Special Conditions'), max_length=150, blank=True, null=True)
  user_did_not_show_up = models.BooleanField(_("User did not show up"), default=False)

  class Meta:
    app_label = "pv"
    verbose_name = _("PV Meeting Appointment")
    verbose_name_plural = _("PV Meetings Appointments")

  def __init__(self, *args, **kwargs):
    super(PVMeetingAppointment, self).__init__(*args, **kwargs)
    self.__original_user_did_not_show_up = self.user_did_not_show_up

  def can_apply(self):
    return self.user.pvuserinfo.can_apply
  can_apply.boolean = True
  can_apply.short_description = _("Can apply")

  def mailing(self, async_mail=None):
    return emails.AppointmentMail(self, async_mail)

  def save(self, *args, **kwargs):
    creating = False
    if not self.pk:
      creating = True

    user_did_not_show_up = False
    if self.user_did_not_show_up and self.user_did_not_show_up != self.__original_user_did_not_show_up:
      user_did_not_show_up = True

    super(PVMeetingAppointment, self).save(*args, **kwargs)

    if creating:
      self.mailing().sendCreated({"appointment": self})

    if user_did_not_show_up:
      self.mailing().sendRequestReapply({"appointment": self})
