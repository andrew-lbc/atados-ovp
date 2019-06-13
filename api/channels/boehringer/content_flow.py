from haystack.query import SQ
from django.db.models import Q
from ovp.apps.projects.models import Project
from ovp.apps.projects.models import Apply
from ovp.apps.organizations.models import Organization

from ovp.apps.channels.content_flow import BaseContentFlow
from ovp.apps.channels.content_flow import NoContentFlow
from ovp.apps.channels.content_flow import CFM

class BoehringerContentFlow(BaseContentFlow):
  source = "default"
  destination = "boehringer"

  def get_filter_searchqueryset_q_obj(self, model_class):
    if model_class == Project:
      return SQ(categories=1)
    elif model_class == Organization:
      return SQ(projects_categories=1)

    raise NoContentFlow

  def get_filter_queryset_q_obj(self, model_class):
    if model_class == Project:
      return Q(categories=1)
    elif model_class == Organization:
      return Q(project__categories=1)
    elif model_class == Apply:
      return Q(project__categories=1)

    raise NoContentFlow

CFM.add_flow(BoehringerContentFlow())
