from ovp.apps.core.emails import BaseMail

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
    return self.sendEmail('atados-askProjectInteractionConfirmation-toVolunteer', 'Ask project confirmation', context)

  def sendAskAboutProjectExperienceToVolunteer(self, context={}):
    """
    Sent to volunteer 2 days after project date or 45 days after start(for recurrent projects)
    """
    return self.sendEmail('atados-askAboutProjectExperience-toVolunteer', 'Ask about project experience', context)

  def sendAskAboutProjectExperienceToOrganization(self, context={}):
    """
    Sent to organization 2 days after project date or 45 days after start(for recurrent projects)
    """
    return self.sendEmail('atados-askAboutProjectExperience-toOrganization', 'Ask about project experience', context)

  def sendProjectReminderToVolunteer(self, context={}):
    """
    Sent to volunteer 3 days before project
    """
    return self.sendEmail('atados-projectReminder-toVolunteer', 'You have a project in 3 days', context)