from graphene import ClientIDMutation, Field, String as String

from graphql_schema import helpers as graphql
from ovp_core.models import (
  AddressComponentType as AddressComponentTypeModel
  AddressComponent as AddressComponentModel
  GoogleRegion as GoogleRegionModel
  GoogleAddress as GoogleAddressModel
  )


AddressComponentTypeNode = graphql.type4model(AddressComponentTypeModel)
AddressComponentNode = graphql.type4model(AddressComponentModel)
GoogleRegionNode = graphql.type4model(GoogleRegionModel)
GoogleAddressNode = graphql.type4model(GoogleAddressModel)

AddressComponentTypeQuery = graphql.list_n_retrieve_query(AddressComponentTypeNode)
AddressComponentQuery = graphql.list_n_retrieve_query(AddressComponentNode)
GoogleRegionQuery = graphql.list_n_retrieve_query(GoogleRegionNode)
GoogleAddressQuery = graphql.retrieve_query(GoogleAddressNode)

Query = graphql.base_query(
  AddressComponentTypeQuery, AddressComponentQuery,
  GoogleRegionQuery, GoogleAddressQuery
  )

GoogleAddressForm = graphql.model2input(GoogleAddressModel)
class MutateGoogleAddress(ClientIDMutation):
  Input = GoogleAddressForm
  address = Field(GoogleAddressNode) # Payload Field
  @classmethod
  def mutate_and_get_payload(cls, input, context, info):
    address=GoogleAddressModel.objects.update_or_create(**input)
    return cls(address=address)

Mutation = graphql.compose_mutation(
  register_google_address=MutateGoogleAddress,
  update_google_address=MutateGoogleAddress,
  )