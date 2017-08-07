from graphql_schema import helpers as graphql

from .lead import Query as leads_query
#-- from .lead import Mutation as leads_mutation
from .skill import Query as skills_query
from .cause import Query as causes_query
from .availability import Query as availabilities_query


Query = graphql.base_query(
  leads_query,
  skills_query,
  causes_query,
  availabilities_query,
  )
"""
Mutation = graphql.base_mutation(
  leads_mutation)
"""