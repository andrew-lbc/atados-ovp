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