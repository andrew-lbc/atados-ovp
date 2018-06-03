from __future__ import absolute_import

from ovp.apps.projects.models import Apply

from channels.default.emails import AtadosScheduledEmail
from celery import task

@task(name='channels.pv.tasks.send_notification_one_day_before_meeting')
def send_ask_project_interaction_confirmation_to_volunteer(apply_pk):
  import pudb;pudb.set_trace()
  try:
    apply = Apply.objects.get(pk=apply_pk)
    AtadosScheduledEmail(apply.user).sendAskProjectInteractionConfirmationToVolunteer({"apply": apply})
  except Apply.DoesNotExist:
    pass
