from __future__ import absolute_import

from celery import task

from channels.pv.models import PVMeetingAppointment

@task(name='channels.pv.tasks.send_notification_one_day_before_meeting')
def send_notification_one_day_before_meeting(appointment_pk):
  try:
    appointment = PVMeetingAppointment.objects.get(pk=appointment_pk)
    appointment.mailing().sendNotification()
  except PVMeetingAppointment.DoesNotExist:
    pass
