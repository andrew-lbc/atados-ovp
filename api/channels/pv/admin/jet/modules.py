import datetime
from django.utils import timezone
from ovp.apps.admin.jet.modules import Indicators
from ovp.apps.users.models import User
from channels.pv.models import PVUserInfo

class PVIndicators(Indicators):
  def init_with_context(self, context):
    print("k")
    r = super(PVIndicators, self).init_with_context(context)
    now = timezone.now()
    able_to_apply = PVUserInfo.objects.filter(can_apply=True)
    day_one_month_before = (now - datetime.timedelta(365/12)).replace(tzinfo=timezone.utc)
    month_users = User.objects.filter(joined_date__gte=day_one_month_before)

    self.users_can_apply_count = able_to_apply.count()
    self.month_users_can_apply_count = month_users.filter(pvuserinfo__in=able_to_apply).count()
    return r