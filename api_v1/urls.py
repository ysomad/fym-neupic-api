from django.urls import path
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    MediaList, MediaDetail, TaskList, AppFunctionList, SubfunctionList
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'
    ),
    url(r'^swagger/$', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'
    ),
    url(r'^redoc/$', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'
    ),

    path('media/', MediaList.as_view(), name='media_list'),
    path('media/<int:pk>/', MediaDetail.as_view(), name='media_detail'),
    path('tasks/', TaskList.as_view({'get': 'list', 'post': 'create'}), name='task_list'),
    path('tasks/<int:pk>/', TaskList.as_view({'get': 'retrieve', 'put': 'update'}), name='task_detail'),
    path('functions/', AppFunctionList.as_view(), name='function_list'),
    path('subfunctions/', SubfunctionList.as_view(), name='subfunction_list'),
]


