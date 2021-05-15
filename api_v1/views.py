from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAdminUser

from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    AppFunctionSerializer, BotSerializer, MediaSerializer, TaskSerializer, 
    TaskDetailSerializer, SubfunctionSerializer, AppSerializer, 
)

from tasks.models import (
    AppFunction, Media, Subfunction, Task, Bot, App, 
)
from tasks.managers import (
    get_enabled_bots, get_new_bot_tasks, get_processing_bot_tasks
)
from tasks.tasks import assign_task_to_bot_with_least_number_of_tasks


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]


    @swagger_auto_schema(responses={200: TaskDetailSerializer})
    def retrieve(self, request, pk):
        instance = self.get_object()
        serializer = TaskDetailSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        """
        Creates new task and starts Celery task to
        assign newly created task to a bot with
        least number of new or processing tasks
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Celery task
        assign_task_to_bot_with_least_number_of_tasks.delay(
            serializer.data['id']
        )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tags__name']
    # permission_classes = [IsAdminUser]


class AppFunctionList(ListAPIView):
    queryset = AppFunction.objects.all()
    serializer_class = AppFunctionSerializer
    permission_classes = [IsAdminUser]


class SubfunctionList(ListAPIView):
    queryset = Subfunction.objects.all()
    serializer_class = SubfunctionSerializer
    permission_classes = [IsAdminUser]


class BotViewSet(ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['get'])
    def new_tasks(self, request, pk):
        bot = self.get_object()
        bot_tasks = get_new_bot_tasks(bot.id)
        task_serializer = TaskSerializer(bot_tasks, many=True)
        return Response(task_serializer.data)

    @action(detail=True, methods=['get'])
    def processing_tasks(self, request, pk):
        bot = self.get_object()
        bot_tasks = get_processing_bot_tasks(bot.id)
        task_serializer = TaskSerializer(bot_tasks, many=True)
        return Response(task_serializer.data)


class BotEnabledList(ListAPIView):
    queryset = get_enabled_bots()
    serializer_class = BotSerializer
    permission_classes = [IsAdminUser]


class AppList(ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAdminUser]


 