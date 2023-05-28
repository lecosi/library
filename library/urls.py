"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import asyncio

from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView as BaseGraphQLView
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from apps.data_source.services import SearchBook


class GraphQLView(BaseGraphQLView):

    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)

        try:
            formatted_error["context"] = error.original_error.context
        except AttributeError:
            pass

        return formatted_error


import strawberry

from strawberry.schema.config import StrawberryConfig


async def get_name() -> str:
    search = SearchBook()
    await search.search_books_in_apis({})
    await asyncio.sleep(1)

    return "Strawberry"


@strawberry.type
class Query:
    name: str = strawberry.field(resolver=get_name)


schema = strawberry.Schema(query=Query,
                           config=StrawberryConfig(auto_camel_case=False))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gql/',
         csrf_exempt(AsyncGraphQLView.as_view(graphiql=True, schema=schema)))
]
