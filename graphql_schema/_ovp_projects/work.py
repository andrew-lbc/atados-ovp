from graphql_schema import helpers as graphql

from ovp_projects.serializers.work import (
  WorkSerializer
  )


WorkSerializer = graphql.drf.serializer2type(WorkSerializer)
Query = graphql.retrieve_query(WorkSerializer)