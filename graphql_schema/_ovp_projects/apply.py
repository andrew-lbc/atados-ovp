from graphql_schema import helpers as graphql

from ovp_projects.serializers.apply import (
  ApplyRetrieveSerializer as ApplySerializer
  )


Apply = graphql.drf.serializer2type(ApplySerializer)
Query = graphql.retrieve_query(Apply)