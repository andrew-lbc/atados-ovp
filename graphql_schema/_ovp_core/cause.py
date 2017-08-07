from graphql_schema import helpers as graphql

from ovp_core.serializers import FullCauseSerializer


"""
from ovp_core.models import Cause as CauseModel
CauseType = helpers.type4model(CauseModel)
"""
CauseType = graphql.drf.serializer2type(FullCauseSerializer)

Query = graphql.list_n_retrieve_query(
  CauseType,
  )