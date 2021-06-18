from typing import Union

from django.http import HttpRequest

from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskSerializer, BotSerializer, TaskDetailSerializer
from config import settings

from tasks.models import Task, Bot
from tasks.tasks import assign_task_to_bot_with_least_number_of_tasks
from tasks.managers import (get_new_bot_tasks, get_processing_bot_tasks, 
    get_disabled_bots, get_enabled_bots, get_all_bot_tasks)


def perform_creation_of_new_task_and_assign_to_bot(
        task_view: ModelViewSet, serializer: TaskSerializer) -> None:
    """
    Creates new task with TaskSerializer
    Starts Celery task to assign created task to a bot with
    least number of new or processing tasks
    """
    task_view.perform_create(serializer)
    assign_task_to_bot_with_least_number_of_tasks.delay(serializer.data['id']) 


def get_bot_tasks_by_status(
        bot_viewset: ModelViewSet, task_status: str) -> TaskSerializer:
    """
    Gets tasks assigned to specific bot with task_status
    """
    bot = bot_viewset.get_object()
    if task_status == Task.Status.NEW:
        tasks = get_new_bot_tasks(bot.id)
    elif task_status == Task.Status.PROCESSING:
        tasks = get_processing_bot_tasks(bot.id)
    return TaskSerializer(tasks, many=True)


def get_bots_by_state(bot_state: str) -> BotSerializer:
    """
    Gets bots with state bot_state
    """
    if bot_state == Bot.State.ENABLED:
        bots = get_enabled_bots()
    elif bot_state == Bot.State.DISABLED:
        bots = get_disabled_bots()
    return BotSerializer(bots, many=True)


def get_permission_classes(
        debug: bool = settings.DEBUG) -> Union[AllowAny, IsAdminUser]:
    """
    Returns permission class depending on debug is True or False
    """
    return [AllowAny] if debug else [IsAdminUser]


def retrieve_task_details(
        task_viewset: ModelViewSet, request: HttpRequest) -> Response:
    """
    Gets Task instance and creating TaskDetailSerializer with it
    Returns serializer data
    """
    instance = task_viewset.get_object()
    task_serializer = TaskDetailSerializer(
        instance, context={'request': request})
    return Response(task_serializer.data)


def create_new_task(
        task_viewset: ModelViewSet, request: HttpRequest) -> Response:
    """
    Creates new task and starting new Celery task if task data
    received from user is valid
    Returns created Task instance
    """
    task_serializer = task_viewset.get_serializer(data=request.data) 
    task_serializer.is_valid(raise_exception=True)
    perform_creation_of_new_task_and_assign_to_bot(
        task_viewset, task_serializer)
    return Response(
        task_serializer.data, status=status.HTTP_201_CREATED, 
        headers=task_viewset.get_success_headers(task_serializer.data)
    )


def delete_all_bot_tasks(
        bot_viewset: ModelViewSet, bot_id: Bot.id) -> Response:
    """
    Deletes all tasks bound to bot with bot_id
    """
    bot_tasks = get_all_bot_tasks(bot_id)
    bot_viewset.perform_destroy(bot_tasks)
    return Response(status=status.HTTP_204_NO_CONTENT)

