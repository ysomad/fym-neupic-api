from django.db import models

from taggit.managers import TaggableManager


class Config(models.Model):
    """
    Config model for storing development and production
    settings for main application
    """

    class Type(models.TextChoices):
        DEV = 'dev'
        PROD = 'prod'
    
    # TODO: add verbose_name for each field with fine description
    type = models.CharField(max_length=8, choices=Type.choices)
    lock_app_after_function = models.BooleanField()
    lock_app_before_function = models.BooleanField()
    lock_main_menu = models.BooleanField()
    amount_try_function = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.type)


class Media(models.Model):
    """
    Model for storing images, video and gifs with different tags
    """

    class Type(models.TextChoices):
        EDITED_IMG = 'edited_image'
        UNEDITED_IMG = 'unedited_image'
        EDITED_VIDEO = 'edited_video'
        UNEDITED_VIDEO = 'unedited_video'
        EDITED_GIF = 'edited_gif'
        UNEDITED_GIF = 'unedited_gif'
        TEMPLATE_GIF = 'template_gif'
        TEMPLATE_VID = 'template_video'

    media = models.FileField(
        upload_to='tasks',
        verbose_name='media which can be gif/vid/img uploaded by user or \
            using as a template media in main application'
    )
    preview = models.URLField(
        max_length=2048, 
        blank=True,
        null=True, 
        verbose_name='URL to media preview'
    )
    type = models.CharField(
        max_length=16, 
        choices=Type.choices,
        verbose_name='type of media'
    )
    tags = TaggableManager(
        blank=True, 
        verbose_name='tags which is needed for media search'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'media'
        verbose_name_plural = 'media'

    def __str__(self):
        return str(self.media)


class Task(models.Model):
    """
    Representation of tasks which is creating by users in main application
    for bots
    """

    class Status(models.TextChoices):
        NEW = 'new'
        PROCESSING = 'processing'
        DONE = 'done'
        ERROR = 'error'
        CANCELED = 'canceled'

    media = models.ManyToManyField(Media, verbose_name='media URL')
    function = models.ForeignKey(
        'AppFunction', verbose_name='app function', on_delete=models.CASCADE
    )
    subfunction = models.ForeignKey(
        'Subfunction', 
        null=True,
        blank=True,
        verbose_name='subfunction of app function', 
        on_delete=models.CASCADE
    )
    bot = models.ForeignKey(
        'Bot', 
        blank=True, 
        null=True, 
        verbose_name='remote bot',
        on_delete=models.CASCADE
    ) 
    status = models.CharField(
        max_length=32, 
        blank=True, 
        choices=Status.choices, 
        default=Status.NEW,
        verbose_name='task status'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='timestamp'
    )

    class Meta:
        db_table = 'task'

    def __str__(self):
        return str(self.id)
        

class AppFunction(models.Model):
    """
    Model for storing application functions with which bots 
    should process media, every function bind to specific
    application
    """

    name = models.CharField(
        max_length=32, unique=True, verbose_name='name of function'
    )
    app = models.ForeignKey(
        'App', 
        on_delete=models.CASCADE, 
        verbose_name='application in which bots will process media'
    )

    class Meta:
        db_table = 'app_function'

    def __str__(self):
        return self.name


class Subfunction(models.Model):
    """
    Model for storing nested functions of application functions
    """

    name = models.CharField(
        max_length=32, unique=True, verbose_name='name of subfunction'
    )
    function = models.ForeignKey(
        'AppFunction', 
        null=True, 
        on_delete=models.CASCADE, 
        verbose_name='function to which subfunction is bound'
    )

    class Meta:
        db_table = 'subfunction'

    def __str__(self):
        return self.name


class Bot(models.Model):
    """
    Bots which will process media from tasks
    """

    class State(models.TextChoices):
        ENABLED = 'enabled'
        DISABLED = 'disabled'

    name = models.CharField(
        max_length=32, unique=True, verbose_name='bot name'
    )
    state = models.CharField(
        max_length=8, 
        choices=State.choices, 
        default=State.DISABLED, 
        verbose_name='bot state'
    )

    class Meta:
        db_table = 'bot'

    def __str__(self):
        return self.name


class App(models.Model):
    """
    Model for storing application names
    """

    name = models.CharField(
        max_length=32, unique=True, verbose_name='application name'
    )

    class Meta:
        db_table = 'app'

    def __str__(self):
        return self.name
