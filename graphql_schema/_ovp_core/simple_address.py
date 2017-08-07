#from graphene import ClientIDMutation, Field, String as String

from graphql_schema import helpers as graphql
from ovp_core.serializers import SimpleAddressSerializer


SimpleAddress = graphql.drf.serializer2type(SimpleAddressSerializer)
Query = graphql.list_n_retrieve_query(
  SimpleAddress,
  )