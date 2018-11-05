from datetime import timedelta
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization
from ovp.apps.projects.models import Job
from ovp.apps.projects.models import Apply
from ovp.apps.projects.models import Project
from ovp.apps.ratings.models import Rating
from ovp.apps.ratings.models import RatingRequest
from ovp.apps.ratings.models import RatingParameter
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
    eta = timezone.now() + timedelta(days=30)
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

def create_rating_request(sender, *args, **kwargs):
  """
  Create rating request when project is closed
  """
  instance = kwargs["instance"]

  if instance.channel.slug == "default" and not kwargs["raw"]:
    try:
      if instance.closed == True and Project.objects.get(pk=instance.pk).closed == False and instance.job:
        for apply in instance.apply_set.all():
          req = RatingRequest.objects.create(requested_user=instance.owner, rated_object=apply.user, object_channel=instance.channel.slug)
          req.rating_parameters.add(RatingParameter.objects.get(slug="volunteer-score"))

          req = RatingRequest.objects.create(requested_user=apply.user, rated_object=instance, object_channel=instance.channel.slug)
          req.rating_parameters.add(RatingParameter.objects.get(slug="project-how-was-it"))
          req.rating_parameters.add(RatingParameter.objects.get(slug="project-score"))
    except Job.DoesNotExist:
      pass
pre_save.connect(create_rating_request, sender=Project)

def update_scores(sender, *args, **kwargs):
  """
  Create rating request when project is closed
  """
  instance = kwargs["instance"]

  if instance.channel.slug == "default" and not kwargs["raw"] and kwargs["created"]:
    obj = instance.rated_object

    if isinstance(obj, User):
      ratings = Rating.objects.filter(rated_object=obj)
      for rating in ratings:
        s = 0
        c = 0
        for answer in rating.answers:
          if answer.parameter.slug == "volunteer-score":
            s += answer.value_quantitative
            c += 1

      if c > 1:
        obj.score = s/c
        obj.save()

    elif isinstance(obj, Project):
      return 'project'
post_save.connect(create_rating_request, sender=Rating)