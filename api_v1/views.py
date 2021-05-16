from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import filters

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    AppFunctionSerializer, BotSerializer, MediaSerializer, TaskSerializer, 
    TaskDetailSerializer, SubfunctionSerializer, AppSerializer, 
)
from .services import (
    create_new_task, get_bot_tasks_by_status, get_bots_by_state
)

from tasks.models import (
    AppFunction, Media, Subfunction, Task, Bot, App, 
)
from tasks.managers import get_template_media


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

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
    filter_backends = [filters.SearchFilter]
    search_fields = ['tags__name']

    @action(detail=False, methods=['get'])
    def templates(self, request):
        template_media = get_template_media()
        task_serializer = self.serializer_class(template_media, many=True)
        return Response(task_serializer.data)


class AppFunctionList(ListAPIView):
    queryset = AppFunction.objects.all()
    serializer_class = AppFunctionSerializer


class SubfunctionList(ListAPIView):
    queryset = Subfunction.objects.all()
    serializer_class = SubfunctionSerializer


class BotViewSet(ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    @action(detail=True, methods=['get'])
    def new_tasks(self, request, pk):
        task_serializer = get_bot_tasks_by_status(self, Task.Status.NEW)
        return Response(task_serializer.data)

    @action(detail=True, methods=['get'])
    def processing_tasks(self, request, pk):
        task_serializer = get_bot_tasks_by_status(self, Task.Status.PROCESSING) 
        return Response(task_serializer.data)

    @action(detail=False, methods=['get'])
    def enabled(self, request):
        serializer = get_bots_by_state(Bot.State.ENABLED)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def disabled(self, request):
        serializer = get_bots_by_state(Bot.State.DISABLED)
        return Response(serializer.data)


class AppList(ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer


 