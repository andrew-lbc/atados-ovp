from graphql_schema import helpers as graphql

from ovp_projects.serializers.job import (
  JobSerializer,
  JobDateSerializer,
  )


Job = graphql.drf.serializer2type(JobSerializer)
JobDate = graphql.drf.serializer2type(JobDateSerializer)

JobQuery = graphql.retrieve_query(Job)
JobDateQuery = graphql.retrieve_query(JobDate)

Query = graphql.base_query(
  JobQuery,
  JobDateQuery,
  )