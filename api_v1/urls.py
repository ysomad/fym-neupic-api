from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .views import (
    MediaViewSet, TaskViewSet, AppFunctionList, SubfunctionList,
    BotViewSet, AppList,
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

# Viewset router
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'media', MediaViewSet)
router.register(r'bots', BotViewSet)

urlpatterns = [
    # Router
    path('', include(router.urls)),

    # Documentation / OpenAPI
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'
    ),
    url(r'^swagger/$', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'
    ),

    # Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Api endpoints
    path('functions/', AppFunctionList.as_view(), name='function_list'),
    path('subfunctions/', SubfunctionList.as_view(), name='subfunction_list'),
    path('apps/', AppList.as_view(), name='app_list'),
]


