from graphql_schema import helpers as graphql

from .apply import Query as apply_query
from .job import Query as job_query
from .project import Query as project_query
from .role import Query as role_query
from .work import Query as work_query


Query = graphql.base_query(
  apply_query,
  job_query,
  project_query,
  role_query,
  work_query,
  )