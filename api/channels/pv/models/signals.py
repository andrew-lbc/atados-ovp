from . import PVMeetingAppointment

from django.db.models.signals import post_save
from datetime import timedelta
from channels.pv import tasks

def appointment_created(sender, *args, **kwargs):
  instance = kwargs["instance"]
  if kwargs["created"] and not kwargs["raw"]:
    tasks.send_notification_one_day_before_meeting.apply_async(
      eta=instance.meeting.date - timedelta(days=1),
      kwargs={"appointment_pk": instance.pk},
    )

post_save.connect(appointment_created, sender=PVMeetingAppointment)

