from graphql_schema import helpers as graphql

from ovp_users.serializers.profile import get_profile_serializers

#
# get_profile_serializers():
#   => (CreateUpdate, Retrieve, Search)
#
ProfileSerializer = get_profile_serializers()[1]

Profile = graphql.drf.serializer2type(ProfileSerializer)
Query = graphql.retrieve_query(
  Profile,
  )