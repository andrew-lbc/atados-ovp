from graphql_schema import helpers

from ovp_core.serializers import SkillSerializer


"""
from ovp_core.models import Skill as SkillModel
SkillType = helpers.type4model(SkillModel)
"""
SkillType = helpers.drf.serializer2type(SkillSerializer)

Query = helpers.list_n_retrieve_query(
  SkillType,
  )