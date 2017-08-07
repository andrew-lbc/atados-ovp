from graphene import ClientIDMutation, Field, String as String

from graphql_schema import helpers as graphql
from ovp_core.models import (
  AddressComponentType as AddressComponentTypeModel
  AddressComponent as AddressComponentModel
  GoogleRegion as GoogleRegionModel
  GoogleAddress as GoogleAddressModel
  )

"""
  * Use models directly 'cause serializers are just subsets
"""
AddressComponentType = graphql.type4model(AddressComponentTypeModel)
AddressComponent = graphql.type4model(AddressComponentModel)
GoogleRegion = graphql.type4model(GoogleRegionModel)
GoogleAddress = graphql.type4model(GoogleAddressModel)

AddressComponentTypeQuery = graphql.list_n_retrieve_query(AddressComponentType)
AddressComponentQuery = graphql.list_n_retrieve_query(AddressComponent)
GoogleRegionQuery = graphql.list_n_retrieve_query(GoogleRegion)
GoogleAddressQuery = graphql.retrieve_query(GoogleAddress)

Query = graphql.base_query(
  AddressComponentTypeQuery, AddressComponentQuery,
  GoogleRegionQuery, GoogleAddressQuery
  )