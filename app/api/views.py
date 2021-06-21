from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.mixins import (
    RetrieveModelMixin, ListModelMixin, CreateModelMixin)
from rest_framework.viewsets import GenericViewSet

from drf_yasg.utils import swagger_auto_schema

from .serializers import (AppFunctionSerializer, BotSerializer, MediaSerializer, 
    TaskSerializer, TaskDetailSerializer, SubfunctionSerializer, AppSerializer, 
    TagSerializer, ConfigSerializer)
from .services import (get_bot_tasks_by_status, 
    get_permission_classes, retrieve_task_details, create_new_task, 
    delete_all_bot_tasks)
from .pagination import MediaPagination

from tasks.models import Task
from tasks.managers import (get_all_configs, get_all_tasks,
    get_all_media, get_all_functions, get_all_subfunctions, get_all_bots, 
    get_all_applications, get_all_tags)


class ConfigViewSet(CreateModelMixin,
                    ListModelMixin,
                    RetrieveModelMixin,
                    GenericViewSet):
    queryset = get_all_configs()
    serializer_class = ConfigSerializer


class TaskViewSet(ModelViewSet):
    queryset = get_all_tasks()
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'bot__name'] 
    permission_classes = get_permission_classes()

    @swagger_auto_schema(responses={200: TaskDetailSerializer})
    def retrieve(self, request, pk):
        return retrieve_task_details(self, request)

    def create(self, request):
        return create_new_task(self, request)


class MediaViewSet(ModelViewSet):
    queryset = get_all_media()
    serializer_class = MediaSerializer
    filterset_fields = ['tags__name', 'type'] 
    permission_classes = get_permission_classes()
    pagination_class = MediaPagination

    @method_decorator(cache_page(60*60))
    def list(self, *args, **kwargs):
        return super(MediaViewSet, self).list(*args, **kwargs)


class AppFunctionList(ListAPIView):
    queryset = get_all_functions()
    serializer_class = AppFunctionSerializer
    permission_classes = get_permission_classes()


class SubfunctionList(ListAPIView):
    queryset = get_all_subfunctions()
    serializer_class = SubfunctionSerializer
    permission_classes = get_permission_classes()
    filterset_fields = ['function__name', 'function__app__name']


class BotViewSet(ModelViewSet):
    queryset = get_all_bots()
    serializer_class = BotSerializer
    filterset_fields = ['state', 'name'] 
    permission_classes = get_permission_classes()

    @action(detail=True, methods=['get'])
    def new_tasks(self, request, pk):
        task_serializer = get_bot_tasks_by_status(self, Task.Status.NEW)
        return Response(task_serializer.data)

    @action(detail=True, methods=['get'])
    def processing_tasks(self, request, pk):
        task_serializer = get_bot_tasks_by_status(self, Task.Status.PROCESSING) 
        return Response(task_serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_tasks(self, request, pk):
        return delete_all_bot_tasks(self, pk)


class AppList(ListAPIView):
    queryset = get_all_applications()
    serializer_class = AppSerializer
    permission_classes = get_permission_classes()


class TagList(ListAPIView):
    queryset = get_all_tags()
    serializer_class = TagSerializer
    permission_classes = get_permission_classes()

    @method_decorator(cache_page(60*60))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

 