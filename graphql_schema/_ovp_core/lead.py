from graphene import ClientIDMutation, Field, String

from graphql_schema import helpers as graphql
from ovp_core.models import Lead as LeadModel


Lead = graphql.type4model(LeadModel)
Query = graphql.list_n_retrieve_query(
  Lead,
  )

class RegisterLead(ClientIDMutation):
  Input = graphql.model2input(LeadModel,
            only_fields=['email', 'name', 'phone', 'country'],
            required=['email'])

  message=String() # Payload Field
  @classmethod
  def mutate_and_get_payload(cls, input, context, info):
    email = input.pop('email')
    lead_created = LeadModel.register(email=email, **input)
    if lead_created:
      return cls(message="Lead successfully created.")
    else:
      return cls(message="Lead successfully updated.")
Mutation = graphql.compose_mutation(
  register_lead=RegisterLead
  )
#----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# TODO: make lead's email an index and pass this function to model
def LeadModel__register(email, **attrs):
  """
  This function assumes that attrs has only valid fields
  The returning boolean is meaningful about it being new.
  """
  # clean up blank fields. (Is it necessary?)
  attrs = {k: v for k, v in attrs.items() if isinstance(v, (int, float)) or v}
  try:
    existing = LeadModel.objects.get(email=email)
    LeadModel.objects.filter(pk=existing.pk).update(**attrs)
    return False
  except (LeadModel.DoesNotExist):
    LeadModel.objects.create(email=email, **attrs)
    return True

LeadModel.register = LeadModel__register
staticmethod(LeadModel.register)