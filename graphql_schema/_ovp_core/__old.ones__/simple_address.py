from graphene import ClientIDMutation, Field, String as String

from graphql_schema import helpers as graphql
from ovp_core.models import SimpleAddress as SimpleAddressModel


SimpleAddressNode = graphql.type4model(SimpleAddressModel)
Query = graphql.list_n_retrieve_query(
  SimpleAddressNode,
  )


SimpleAddressForm = graphql.model2input(SimpleAddressModel)
class MutateAddress(ClientIDMutation):
  Input = SimpleAddressForm
  address = Field(SimpleAddressNode) # Payload Field
  @classmethod
  def mutate_and_get_payload(cls, input, context, info):
    address=SimpleAddressModel.objects.update_or_create(**input)
    return cls(address=address)
    """
    if 'id' in input:
      address_id = input.pop('id')
      try:
        SimpleAddress.objects.filter(pk=address_id).update(**input)
        address=SimpleAddress.objects.get(pk=address_id)
      except (SimpleAddress.DoesNotExist):
        address=None
    if address is None:
      address=SimpleAddress.objects.create(**input)
    """
Mutation = graphql.compose_mutation(
  register_address=MutateAddress,
  update_address=MutateAddress,
  )