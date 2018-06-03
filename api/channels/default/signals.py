from datetime import timedelta
from django.db.models.signals import post_save
from ovp.apps.projects.models import Apply
from channels.default import tasks
from django.utils import timezone

def schedule_ask_project_interaction_to_volunteer(sender, *args, **kwargs):
  """
  Schedule task for 7 days after apply asking if user has received contact from organization
  """
  instance = kwargs["instance"]

  if instance.channel.slug == "default" and kwargs["created"] and not kwargs["raw"]:
    tasks.send_ask_project_interaction_confirmation_to_volunteer.apply_async(
      eta=timezone.now() + timedelta(days=7),
      kwargs={"apply_pk": instance.pk},
    )

post_save.connect(schedule_ask_project_interaction_to_volunteer, sender=Apply)