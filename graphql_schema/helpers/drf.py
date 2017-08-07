from graphene_django import DjangoObjectType

from .model import type4model


def serializer2type(serializer, name=None):
  serializer_meta = serializer.Meta
  if hasattr(serializer_meta, 'fields'):
    only_fields = serializer_meta.fields.copy()
  else:
    only_fields = None

  sr_declared_fields = serializer._declared_fields
  if len(sr_declared_fields) is not 0:
    pass # TODO : filter fields and declare resolvers when fields not present on model


  _type_ = type4model(serializer_meta.model,
    obj_type=DjangoObjectType,
    meta_attrs={
      'only_fields': only_fields,
      }, name=name)

  _type_._from_drf_serializer = True
  _type_._drf_serializer = serializer
  return _type_



def __resolve_list_n_retrieve_names(type_node, single_name=None, list_name=None):
  if not (single_name and list_name):
    base_model_name = __normalize_model_name(type_node._meta.model)

  if single_name is None:
    single_name = base_model_name

  if list_name is None:
    list_name = 'list_' + faux_pluralize(base_model_name)

  return (single_name, list_name,)

def list_n_retrieve_query(type_node, single_name=None, list_name=None):
  single_name, list_name = __resolve_list_n_retrieve_names(
                              type_node, single_name=None, list_name=None)
  return type('Query', (AbstractType, ), {
    single_name: relay.Node.Field(type_node),
    list_name: DjangoFilterConnectionField(type_node),
    })


def serializer2list_n_retrieve_query(serializer,
  type_node=None, single_name=None, list_name=None
  ):
  if type_node is None:
    type_node = serializer2type(serializer)