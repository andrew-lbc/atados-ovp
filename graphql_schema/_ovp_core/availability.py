from graphql_schema import helpers as graphql

from ovp_core.serializers import AvailabilitySerializer


"""
from ovp_core.models import Availability as AvailabilityModel
Availability = graphql.type4model(AvailabilityModel, meta_attrs={
  #'enum_fields': ('weekday', 'period', ),  # TODO : review about removing this
  'exclude_fields': ('period_index', ),
  })
"""
Availability = graphql.drf.serializer2type(AvailabilitySerializer)

Query = graphql.list_n_retrieve_query(
  Availability,
  list_name='list_availabilities'
  )