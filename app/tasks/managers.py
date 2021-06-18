from .models import App, Task, Bot, Media, Config, AppFunction, Subfunction
from taggit.models import Tag


def get_all_tags():
    """
    Returns QuerySet of all django-taggit tags
    """
    return Tag.objects.all()


def get_all_applications():
    """
    Returns QuerySet of all applications
    """
    return App.objects.all()


def get_all_bots():
    """
    Returns QuerySet of all subfunctions
    """ 
    return Bot.objects.all()


def get_all_subfunctions():
    """
    Returns QuerySet of all subfunctions
    """
    return Subfunction.objects.all()


def get_all_functions():
    """
    Returns QuerySet of all application functions
    """
    return AppFunction.objects.all()


def get_all_media():
    """
    Returns QuerySet of all media
    """
    return Media.objects.all()


def get_all_tasks():
    """
    Returns QuerySet of all tasks
    """
    return Task.objects.all()



def get_all_configs():
    """
    Returns QuerySet of all configs
    """
    return Config.objects.all()


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


def get_disabled_bots():
    """
    Returns QuerySet of bots with disabled state
    """
    return Bot.objects.filter(state=Bot.State.DISABLED)


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


def get_all_bot_tasks(bot_id):
    """
    Returns QuerySet of all tasks of specific bot with bot_id
    """
    return Task.objects.filter(bot=bot_id)


def get_template_media():
    """
    Returns QuerySet of media with state 'template'
    """
    return Media.objects.filter(state=Media.State.TEMPLATE)