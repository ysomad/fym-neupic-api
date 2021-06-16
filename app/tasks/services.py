import operator

from .managers import get_enabled_bots, get_processing_and_new_bot_tasks
from .models import Bot, Task


def get_bots_tasks_count(bots: Bot) -> dict:
    """
    Returns dictionary with Bot.id key and bot tasks count value
    """
    bot_tasks_count = {}
    for bot in bots:
        bot_id = bot.id
        bot_tasks = get_processing_and_new_bot_tasks(bot_id)
        bot_tasks_count[bot_id] = bot_tasks.count()
    return bot_tasks_count


def find_bot_with_least_number_of_tasks() -> Bot.id:
    """
    Returns Bot.id with least number of new or processing tasks
    """
    bots = get_enabled_bots()
    bot_tasks_count = get_bots_tasks_count(bots)
    return min(bot_tasks_count.items(), key=operator.itemgetter(1))[0]
    

def assign_task_to_bot(task_id: int, bot_id: int) -> None:
    """
    Assigns task with task_id to bot with bot_id
    """
    task = Task.objects.get(pk=task_id)
    task.bot = Bot.objects.get(pk=bot_id)
    task.save()