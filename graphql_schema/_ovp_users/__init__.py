from graphql_schema import helpers as graphql

from .user import Query as user_query
from .profile import Query as profile_query


Query = graphql.base_query(
  user_query,
  profile_query,
  )