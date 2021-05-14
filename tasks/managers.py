from .models import Task, Bot


def get_new_tasks():
    """
    Returns QuerySet of all new tasks not assigned to any bot
    """
    return Task.objects.filter(status=Task.Status.NEW, bot=None)


def get_enabled_bots():
    """
    Returns QuerySet of bots with enabled state
    """
    return Bot.objects.filter(state=Bot.State.ENABLED)


def get_new_bot_tasks(bot_id):
    """
    Returns QuerySet of tasks with status 'new' of specific
    bot with bot_id 
    """
    return Task.objects.filter(bot=bot_id, status=Task.Status.NEW)


def get_processing_bot_tasks(bot_id):
    """
    Returns QuerySet of tasks with status 'processing' of specific
    bot with bot_id
    """
    return Task.objects.filter(bot=bot_id, status=Task.Status.PROCESSING)


def get_processing_and_new_bot_tasks(bot_id):
    """
    Returns QuerySet of tasks with status 'processing and 'new' of
    specific bot with bot_id
    """
    return Task.objects.filter(bot=bot_id).exclude(status=Task.Status.DONE)
