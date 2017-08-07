from graphene import ClientIDMutation, Field, String

from graphql_schema import helpers as graphql
from ovp_uploads.models import UploadedImage as UploadedImageModel


UploadedImage = graphql.resolver_type4model(UploadedImageModel, {
  'image_url': (String, 'get_image_url'),
  'image_small_url': (String, 'get_image_small_url'),
  'image_medium_url': (String, 'get_image_medium_url'),
  'image_large_url': (String, 'get_image_large_url'),
  }, exclude_fields=('image', 'image_small', 'image_medium', 'image_large'))


Query = graphql.retrieve_query(
  UploadedImage,
  )