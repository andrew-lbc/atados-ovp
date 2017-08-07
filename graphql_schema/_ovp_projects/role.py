from graphql_schema import helpers as graphql

from ovp_projects.serializers.role import (
  VolunteerRoleSerializer as VolunteerRoleSerializer
  )


VolunteerRole = graphql.drf.serializer2type(VolunteerRoleSerializer)
Query = graphql.retrieve_query(VolunteerRole)