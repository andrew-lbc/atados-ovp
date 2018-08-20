from __future__ import absolute_import

from ovp.apps.projects.models import Apply
from ovp.apps.projects.models import Project

from channels.default.emails import AtadosScheduledEmail
from celery import task

@task(name='channels.default.tasks.send_ask_project_interaction_confirmation_to_volunteer')
def send_ask_project_interaction_confirmation_to_volunteer(apply_pk):
  try:
    apply = Apply.objects.get(pk=apply_pk)
    AtadosScheduledEmail(apply.user).sendAskProjectInteractionConfirmationToVolunteer({"apply": apply})
  except Apply.DoesNotExist:
    pass

@task(name='channels.default.tasks.send_project_reminder_to_volunteer')
def send_project_reminder_to_volunteer(apply_pk):
  try:
    apply = Apply.objects.get(pk=apply_pk)
    AtadosScheduledEmail(apply.user).sendProjectReminderToVolunteer({"apply": apply})
  except Apply.DoesNotExist:
    pass

@task(name='channels.default.tasks.send_ask_about_project_experience_to_volunteer')
def send_ask_about_project_experience_to_volunteer(apply_pk):
  try:
    apply = Apply.objects.get(pk=apply_pk)
    AtadosScheduledEmail(apply.user).sendAskAboutProjectExperienceToVolunteer({"apply": apply})
  except Apply.DoesNotExist:
    pass

@task(name='channels.default.tasks.send_ask_about_project_experience_to_organization')
def send_ask_about_project_experience_to_organization(project_pk):
  try:
    project = Project.objects.get(pk=project_pk)
    if hasattr(project, 'work'):
      AtadosScheduledEmail(project.owner).sendAskAboutProjectWorkExperienceToOrganization({"project": project})
    else:
      AtadosScheduledEmail(project.owner).sendAskAboutProjectJobExperienceToOrganization({"project": project})
  except Project.DoesNotExist:
    pass