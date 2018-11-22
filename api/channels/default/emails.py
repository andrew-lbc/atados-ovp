from ovp.apps.core.emails import BaseMail
from urllib.parse import quote
from urllib.parse import urlencode

class EmailClientRouterHelper():
  BASE_URL = "https://www.atados.com.br"
  MAIL_ROUTINE_URL = {
    'ask_project_exp': {
      'organization': 'https://docs.google.com/forms/d/1cYbjzxC-ETSSVdz76I62t0oToRs7OXZCGEpm7taryY8/viewform',
      'volunteer': 'https://docs.google.com/forms/d/1MdBYnmnH_EAiku1m0yeEPg7jTLyW7uzCJ5GcYXiMQkc/viewform',
    }
  }
  MAIL_ROUTINE_MONITORING_BASE_CONFIRM_URL = "https://docs.google.com/forms/d/1zelGspQUTntp8hUSJXzLTPQXt0G3COPQ3ZYHR5blOj8/viewform"
  MAIL_ROUTINE_MONITORING_BASE_REFUTE_URL  = "https://docs.google.com/forms/d/1ZXcVgWENGWfCDnDDJ-JcFUFrHOcgRvWlK5Y1VZdniUY/viewform"

  def edit_project_url(self, organization_slug, project_slug):
    return u"{}/painel/ong/{}/vaga/{}".format(self.BASE_URL, organization_slug, project_slug)

  def mail_ask_about_project_experience_url(self, to, obj):
    base_url = self.MAIL_ROUTINE_URL['ask_project_exp'][to]
    if base_url:
      if to == 'volunteer':
        project = obj.project
        query_string = urlencode({ # Fields on the form
          'entry.221477937': obj.email,
          'entry.1166737892': project.organization.name,
          'entry.1735336797': project.name,
        })
      else:
        project = obj
        query_string = urlencode({ # Fields on the form
          'entry.1023722142': project.owner.email,
          'entry.1963768658': project.organization.name,
          'entry.321022436': project.name,
          'entry.742260943': project.applied_count,
        })
      return "{}?edit_requested=true&{}".format(base_url, query_string)
    else:
      pass

  def mail_routine_monitoring_build_form_url(self, confirmation, apply):
    query_string = urlencode({ # Fields on the form
      "entry.1864240677": apply.email,
      "entry.701739852": apply.project.organization.name,
    })

    if confirmation:
      base_url = self.MAIL_ROUTINE_MONITORING_BASE_CONFIRM_URL
    else:
      base_url = self.MAIL_ROUTINE_MONITORING_BASE_REFUTE_URL
    return u"{}?edit_requested=true&{}".format(base_url, query_string)

class AtadosScheduledEmail(BaseMail):
  """
  This class is responsible for firing atados specific scheduled emails
  """
  def __init__(self, recipient_user, async_mail=None):
    super(AtadosScheduledEmail, self).__init__(recipient_user.email, channel="default", async_mail=async_mail, locale=recipient_user.locale)

  def sendAskProjectInteractionConfirmationToVolunteer(self, context={}):
    """
    Sent 7 days after user applies to a project
    """
    router = EmailClientRouterHelper()
    context.update({
      "confirm_url": router.mail_routine_monitoring_build_form_url(True, context["apply"]),
      "refute_url": router.mail_routine_monitoring_build_form_url(False, context["apply"])
    })
    return self.sendEmail('atados-askProjectInteractionConfirmation-toVolunteer', 'Ask project confirmation', context)

  def sendAskAboutProjectExperienceToVolunteer(self, context={}):
    """
    Sent to volunteer 2 days after project date or 45 days after start(for recurrent projects)
    """
    router = EmailClientRouterHelper()
    context.update({
      "feedback_form_url": router.mail_ask_about_project_experience_url("volunteer", context["apply"]),
    })
    return self.sendEmail('atados-askAboutProjectExperience-toVolunteer', 'Ask about project experience', context)

  def sendAskAboutProjectJobExperienceToOrganization(self, context={}):
    """
    Sent to organization 2 days after project date or 30 days after start(for recurrent projects)
    """
    router = EmailClientRouterHelper()
    context.update({
      "feedback_form_url": router.mail_ask_about_project_experience_url("organization", context["project"]),
      "edit_project_url": router.edit_project_url(context["project"].organization.slug, context["project"].slug)
    })
    return self.sendEmail('atados-askAboutProjectJobExperience-toOrganization', 'Ask about project experience', context)

  def sendProjectReminderToVolunteer(self, context={}):
    """
    Sent to volunteer 3 days before project
    """
    return self.sendEmail('atados-projectReminder-toVolunteer', 'You have a project in 3 days', context)

  def sendAskAboutProjectWorkExperienceToOrganization(self, context={}):
    """
    Sent to organization 2 days after project date or 30 days after start(for recurrent projects)
    """
    router = EmailClientRouterHelper()
    context.update({
      "feedback_form_url": router.mail_ask_about_project_experience_url("organization", context["project"]),
      "edit_project_url": router.edit_project_url(context["project"].organization.slug, context["project"].slug)
    })
    return self.sendEmail('atados-askAboutProjectWorkExperience-toOrganization', 'Ask about project experience', context)

  def sendRatingRequestReminder(self, context={}):
    """
    Sent to volunteer after project closes
    """
    pass