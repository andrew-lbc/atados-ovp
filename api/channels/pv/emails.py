from ovp.apps.core.emails import BaseMail

class AppointmentMail(BaseMail):
  """
  This class is responsible for firing emails about appointments
  """
  def __init__(self, appointment, async_mail=None):
    super(AppointmentMail, self).__init__(appointment.user.email, channel=appointment.channel.slug, async_mail=async_mail, locale=appointment.user.locale)

  def sendCreated(self, context={}):
    """
    Sent when user creates an appointment
    """
    return self.sendEmail('appointmentCreated', 'Appointment created', context)

  def sendNotification(self, context={}):
    """
    Sent one day before appointment
    """
    return self.sendEmail('appointmentNotification', 'Appointment notification', context)

class UserInfoMail(BaseMail):
  """
  This class is responsible for firing emails about approvals
  """
  def __init__(self, user_info, async_mail=None):
    super(UserInfoMail, self).__init__(user_info.user.email, channel=user_info.channel.slug, async_mail=async_mail, locale=user_info.user.locale)

  def sendApproved(self, context={}):
    """
    Sent when user gets approved to apply
    """
    return self.sendEmail('userApplyingApproved', 'You are approved.', context)
