from typing import Union
from rest_framework.permissions import IsAdminUser, AllowAny

from .serializers import TaskSerializer, BotSerializer

from config import settings
from tasks.models import Task, Bot
from tasks.tasks import assign_task_to_bot_with_least_number_of_tasks
from tasks.managers import (
    get_new_bot_tasks, get_processing_bot_tasks, get_disabled_bots,
    get_enabled_bots
)


def create_new_task(task_view, serializer) -> None:
    """
    Creates new task with TaskSerializer
    Starts Celery task to assign created task to a bot with
    least number of new or processing tasks
    """
    task_view.perform_create(serializer)
    assign_task_to_bot_with_least_number_of_tasks.delay(serializer.data['id']) 


def get_bot_tasks_by_status(bot_viewset, task_status) -> TaskSerializer:
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
