from .helpers import compose_schema

from ._ovp_core import Query as core_query
from ._ovp_organizations import Query as organizations_query
from ._ovp_projects import Query as projects_query
from ._ovp_uploads import Query as uploads_query
from ._ovp_users import Query as users_query



root = compose_schema(
  queries=(
    core_query,
    organizations_query,
    projects_query,
    uploads_query,
    users_query,
    ),
  )