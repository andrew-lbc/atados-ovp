from graphql_schema import helpers as graphql

from .organization import Query as organizations_query


Query = graphql.base_query(
  organizations_query,
  )