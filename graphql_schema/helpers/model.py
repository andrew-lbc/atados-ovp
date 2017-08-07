from graphene import relay, AbstractType, ObjectType, Schema, Field
from graphene.types.structures import NonNull
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.converter import convert_django_field_with_choices


def enum4model_field(model, field_name):  # TODO : review about removing this
  if not hasattr(model, field_name):
    raise("Field '{}' does not exists in '{}' model.").format(field_name, model.__name__)
  else:
    field = model._meta.get_field(field_name)
    if not hasattr(field, 'choices') or len(field.choices) is 0:
      raise("Looks like '{}' from '{}' is not a choices field.").format(field_name, model.__name__)

  return convert_django_field_with_choices(field)


def _type4model(model, meta_attrs=None):
  type_attrs = {}
  if meta_attrs is None:
    meta_attrs = {'model':model}
  else:
    meta_attrs = meta_attrs.copy()
    meta_attrs['model'] = model

    if 'enum_fields' in meta_attrs: # TODO : review about removing this
      for field_name in meta_attrs['enum_fields']:
        type_attrs[field_name] = enum4model_field(model, field_name)
      del meta_attrs['enum_fields']

  if not 'interfaces' in meta_attrs:
    meta_attrs['interfaces'] = (relay.Node, )
  type_attrs['Meta'] = type('Meta', (), meta_attrs)

  return type_attrs

def type4model(model, obj_type=DjangoObjectType, meta_attrs=None, name=None):
  type_attrs = _type4model(model, meta_attrs)
  return type(name or model.__name__, (obj_type, ), type_attrs)



def base_query(*queries):
  return type('Query', (*queries, ObjectType, ), {})

def base_mutation(*mutations):
  return type('Mutation', (*mutations, ObjectType, ), {})


def compose_schema(queries=(), mutations=()):
  schema = {}
  if queries is not None and len(queries) > 0:
    schema['query'] = base_query(*queries)
  if mutations is not None and len(mutations) > 0:
    schema['mutation'] = base_mutation(*mutations)
  return Schema(**schema)


import re
def __normalize_model_name(model):
  terms = re.findall('[A-Z][a-z0-9_]+', model.__name__)
  return '_'.join([term.lower() for term in terms ])

def faux_pluralize(word):
  return word + 's'

def retrieve_query(type_node, single_name=None):
  if not single_name:
    single_name = __normalize_model_name(type_node._meta.model)

  return type('Query', (AbstractType, ), {
    single_name: relay.Node.Field(type_node),
    })

def list_n_retrieve_query(type_node, single_name=None, list_name=None):
  if not (single_name and list_name):
    base_model_name = __normalize_model_name(type_node._meta.model)

  if single_name is None:
    single_name = base_model_name

  if list_name is None:
    list_name = 'list_' + faux_pluralize(base_model_name)

  return type('Query', (AbstractType, ), {
    single_name: relay.Node.Field(type_node),
    list_name: DjangoFilterConnectionField(type_node),
    })



from collections import namedtuple

from graphene_django.types import construct_fields
from graphene.types.utils import yank_fields_from_attrs
__fields_opts = namedtuple('fields_opts', ['model', 'fields', 'registry', 'only_fields', 'exclude_fields'])

def model2input(model, **opts):
  """
  **opts:
    model -- Django Model
    only_fields -- Subset of fields to be used (overhidden in inheritance)
    exclude_fields -- List of fields to exclude (overhidden in inheritance)

  All fields are loaded into Input's attrs in the case of
  neither 'only_fields' or 'exclude_fields' being declared.
  """
  fields_opts = __fields_opts(model, [], None, # model, fields, registry
    opts.get('only_fields', []),
    opts.get('exclude_fields', []),
    )

  input_fields = yank_fields_from_attrs(
    construct_fields(fields_opts),
    _as=Field
    )

  # Make required fields non-null
  if 'required' in opts:
    for field_name in opts['required']:
      field = input_fields[field_name]
      if not isinstance(field._type, NonNull):
        field._type = NonNull(field._type)

  # TODO: Remove  non-null attr inherited from models | Does it make sense?

  return type('Input', (), input_fields)


def compose_mutation(**actions):
  mutations = dict([
    (action, mutation.Field()) for action, mutation in actions.items()]
    )
  return type('Mutation', (AbstractType,), mutations)


def default_model_mutate_method(return_node_type):
  if not isinstance(return_node_type, DjangoObjectType):
    raise TypeError(
      "Expected instance of 'DjangoObjectType', got '{}'",
      return_node_type.__class__.__name__
      )
  def mutate_and_get_payload(cls, input, context, info):
    pass






def __construct_field_resolver(func_name):
  def resolver(self, args, context, info):
    return getattr(self.instance, func_name)()
  return resolver

def __construct_field_static_resolver(method):
  def resolver(self, args, context, info):
    return method(self.instance)
  return resolver

def resolver_type4model(model, mappings=None, exclude_fields=None,
                        obj_type=DjangoObjectType):
  base_type = _type4model(model,{
    'exclude_fields': exclude_fields,
    })

  for field, info in mappings.items():
    qltype, resolver = info
    if isinstance(resolver, str):
      if not hasattr(model, resolver):
        raise AttributeError("'{}' not present on '{}'.".format(resolver, model.__name__))
        resolver = __construct_field_resolver(resolver)
    elif callable(resolver):
      resolver = __construct_field_static_resolver(resolver)

    base_type[field] = qltype()
    base_type['resolve_'+field] = resolver

  return type(model.__name__, (obj_type, ), base_type)