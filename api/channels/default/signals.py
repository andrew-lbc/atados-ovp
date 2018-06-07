from datetime import timedelta
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from ovp.apps.projects.models import Apply
from ovp.apps.projects.models import Project
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

def schedule_project_reminder_to_volunteer(sender, *args, **kwargs):
  """
  Schedule task for 3 days before project to remind volunteer
  """
  instance = kwargs["instance"]
  project = instance.project

  if instance.channel.slug == "default" and kwargs["created"] and not kwargs["raw"]:
    if hasattr(project, "job"):
      tasks.send_project_reminder_to_volunteer.apply_async(
        eta=project.job.start_date - timedelta(days=3),
        kwargs={"apply_pk": instance.pk},
      )
post_save.connect(schedule_project_reminder_to_volunteer, sender=Apply)

def calculate_experience_email_eta(project):
  eta = None
  if hasattr(project, "work"):
    eta = timezone.now() + timedelta(days=45)
  elif hasattr(project, "job"):
    eta = project.job.end_date + timedelta(days=2)

  return eta

def schedule_ask_about_project_experience_to_volunteer(sender, *args, **kwargs):
  """
  Schedule task after apply asking about project experience
  """
  instance = kwargs["instance"]
  project = instance.project

  if instance.channel.slug == "default" and kwargs["created"] and not kwargs["raw"]:
    eta = calculate_experience_email_eta(project)
    if eta:
      tasks.send_ask_about_project_experience_to_volunteer.apply_async(eta=eta, kwargs={"apply_pk": instance.pk})
post_save.connect(schedule_ask_about_project_experience_to_volunteer, sender=Apply)

def schedule_ask_about_project_experience_to_organization(sender, *args, **kwargs):
  """
  Schedule task after project publishing asking about project experience
  """
  instance = kwargs["instance"]

  if instance.channel.slug == "default" and not kwargs["raw"]:
    if instance.published == True and (instance.pk == None or Project.objects.get(pk=instance.pk).published == False):
      eta = calculate_experience_email_eta(instance)
      if eta:
        tasks.send_ask_about_project_experience_to_organization.apply_async(eta=eta, kwargs={"project_pk": instance.pk})
pre_save.connect(schedule_ask_about_project_experience_to_organization, sender=Project)