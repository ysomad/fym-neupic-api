from tasks.models import Task
from django.urls import path
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    MediaList, MediaDetail, TaskViewSet, AppFunctionList, SubfunctionList
)

schema_view = get_schema_view(
    openapi.Info(
        title='FYM bot tasks API',
        default_version='v1',
        description='API to create new tasks for bots',
        contact=openapi.Contact(email='alex@fym.team'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

task_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
task_detail = TaskViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})

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

    path('tasks/', task_list, name='task_list'),
    path('tasks/<int:pk>/', task_detail, name='task_detail'),

    path('functions/', AppFunctionList.as_view(), name='function_list'),
    path('subfunctions/', SubfunctionList.as_view(), name='subfunction_list'),
]


