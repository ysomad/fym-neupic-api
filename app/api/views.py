from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from taggit.models import Tag

from .serializers import (AppFunctionSerializer, BotSerializer, MediaSerializer, 
    TaskSerializer, TaskDetailSerializer, SubfunctionSerializer, AppSerializer, 
    TagSerializer, ConfigSerializer)
from .services import (create_new_task, get_bot_tasks_by_status, 
    get_permission_classes)

from tasks.models import (AppFunction, Media, Subfunction, 
    Task, Bot, App, Config)
from tasks.managers import get_all_bot_tasks


class ConfigListCreateAPIView(ListCreateAPIView):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ['status', 'bot__name'] 
    permission_classes = get_permission_classes()

    @swagger_auto_schema(responses={200: TaskDetailSerializer})
    def retrieve(self, request, pk):
        instance = self.get_object()
        serializer = TaskDetailSerializer(
            instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        create_new_task(self, serializer)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, 
            headers=self.get_success_headers(serializer.data)
        )


class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filterset_fields = ['tags__name', 'type'] 
    permission_classes = get_permission_classes()

    @method_decorator(cache_page(60*60))
    def list(self, *args, **kwargs):
        return super(MediaViewSet, self).list(*args, **kwargs)


class AppFunctionList(ListAPIView):
    queryset = AppFunction.objects.all()
    serializer_class = AppFunctionSerializer
    permission_classes = get_permission_classes()


class SubfunctionList(ListAPIView):
    queryset = Subfunction.objects.all()
    serializer_class = SubfunctionSerializer
    permission_classes = get_permission_classes()
    filterset_fields = ['function__name', 'function__app__name']


class BotViewSet(ModelViewSet):
    queryset = Bot.objects.all()
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
        bot_tasks = get_all_bot_tasks(pk)
        if bot_tasks:
            self.perform_destroy(bot_tasks)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AppList(ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = get_permission_classes()


class TagList(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = get_permission_classes()

    @method_decorator(cache_page(60*60))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

 