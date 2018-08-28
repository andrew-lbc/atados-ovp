from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from ovp.apps.admin.jet.modules import OVPRecentActions
from channels.pv.admin.jet.modules import PVIndicators
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.dashboard import modules
from jet.utils import get_admin_site_name

class PVIndexDashboard(Dashboard):
  columns = 3

  def init_with_context(self, context):
    self.available_children.append(modules.LinkList)
    self.available_children.append(modules.Feed)

    site_name = get_admin_site_name(context)

    # append a link list module for "quick links"
    self.children.append(modules.LinkList(
      _('Quick links'),
      layout='inline',
      draggable=False,
      deletable=False,
      collapsible=False,
      children=[
          [_('Return to site'), '/'],
          [_('Change password'),
           reverse('%s:password_change' % site_name)],
          [_('Log out'), reverse('%s:logout' % site_name)],
      ],
      column=0,
      order=0
    ))

    # append an app list module for "Applications"
    self.children.append(modules.AppList(
      _('Applications'),
      exclude=('auth.*',),
      column=1,
      order=0
    ))

    # append an app list module for "Administration"
    self.children.append(modules.AppList(
      _('Administration'),
      models=('auth.*',),
      column=2,
      order=0
    ))

    # append a recent actions module
    self.children.append(OVPRecentActions(
      _('Recent Actions'),
      10,
      column=0,
      order=1
    ))   

    # append a recent actions module
    self.children.append(PVIndicators(
      _('Indicators'),
    ))