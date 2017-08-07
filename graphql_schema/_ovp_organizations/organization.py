from graphql_schema import helpers as graphql

from ovp_organizations.serializers import (
  OrganizationSearchSerializer as OrganizationSerializer
  )


Organization = graphql.drf.serializer2type(OrganizationSerializer)
Query = graphql.retrieve_query(Organization)