from rest_framework import schemas
from rest_framework import decorators
from rest_framework import response
from rest_framework_swagger import renderers

@decorators.api_view()
@decorators.renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def schema_view(request):
  generator = schemas.SchemaGenerator(title='Store API')
  schema = generator.get_schema(request=request)
  return response.Response(schema)
