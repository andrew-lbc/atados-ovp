from graphql_schema import helpers as graphql

from ovp_projects.serializers.project import (
  ProjectRetrieveSerializer as ProjectSerializer
  )

# TODO: Project's serializers have filters on 'to_representation'
Project = graphql.drf.serializer2type(ProjectSerializer)
Query = graphql.retrieve_query(Project)