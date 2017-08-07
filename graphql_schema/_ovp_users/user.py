from graphene import AbstractType, relay

from graphql_schema import helpers as graphql

from ovp_users.serializers.user import (
  CurrentUserSerializer,
  LongUserPublicRetrieveSerializer as PublicUserSerializer,
  )


PublicUser = graphql.drf.serializer2type(PublicUserSerializer)
CurrentUser = graphql.drf.serializer2type(CurrentUserSerializer, name='CurrentUser')

class Query(AbstractType):
  current_user = relay.Node.Field(CurrentUser)
  public_user = relay.Node.Field(PublicUser)
  def resolve_current_user(self, args, context, info):
    return context.user