"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


import ovp_users.urls
import ovp_projects.urls
import ovp_uploads.urls
import ovp_projects.urls
import ovp_search.urls
import ovp_organizations.urls

try:
    import docs.urls as docs_urls
except:
    docs_urls = []

try:
    import graphql_schema.urls as graphql_urls
except:
    graphql_urls = []


urlpatterns = [
    # Admin panel
    url(r'^admin/', admin.site.urls),

    # API Documentation
    url(r'^docs/', include(docs_urls)),

    # GraphQL endpoint
    url(r'^graphql/', include(graphql_urls)),

    # User module endpoints
    url(r'^', include(ovp_users.urls)),

    # Project module endpoints
    url(r'^', include(ovp_projects.urls)),

    # Organization module endpoints
    url(r'^', include(ovp_organizations.urls)),

    # Upload module endpoints
    url(r'^', include(ovp_uploads.urls)),

    # Search module endpoints
    url(r'^', include(ovp_search.urls))
]
