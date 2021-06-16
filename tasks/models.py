from django.db import models

from taggit.managers import TaggableManager


class Config(models.Model):
    """
    Config model for storing development and production
    settings for Neupic application
    """

    class Type(models.TextChoices):
        DEV = 'dev'
        PROD = 'prod'
    
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

    media = models.FileField(upload_to='tasks')
    preview = models.URLField(max_length=2048, blank=True, null=True)
    type = models.CharField(max_length=16, choices=Type.choices)
    tags = TaggableManager(blank=True)
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

    media = models.ManyToManyField(Media)
    function = models.ForeignKey(
        'AppFunction', verbose_name='function', on_delete=models.CASCADE
    )
    subfunction = models.ForeignKey(
        'Subfunction', 
        null=True,
        blank=True,
        verbose_name='subfunction', 
        on_delete=models.CASCADE
    )
    bot = models.ForeignKey(
        'Bot', 
        blank=True, 
        null=True, 
        verbose_name='bot name',
        on_delete=models.CASCADE
    ) 
    status = models.CharField(
        max_length=32, blank=True, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task'

    def __str__(self):
        return str(self.id)
        

class AppFunction(models.Model):
    """
    Model for storing application functions with which the 
    bot should process media, every function bind to specific
    application
    """

    name = models.CharField(
        max_length=32, unique=True, verbose_name='function'
    )
    app = models.ForeignKey('App', on_delete=models.CASCADE)

    class Meta:
        db_table = 'app_function'

    def __str__(self):
        return self.name


class Subfunction(models.Model):
    """
    Model for storing nested functions of application functions
    """

    name = models.CharField(
        max_length=32, unique=True, verbose_name='subfunction'
    )
    function = models.ForeignKey(
        'AppFunction', null=True, on_delete=models.CASCADE
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

    name = models.CharField(max_length=32, unique=True)
    state = models.CharField(
        max_length=8, choices=State.choices, default=State.DISABLED
    )

    class Meta:
        db_table = 'bot'

    def __str__(self):
        return self.name


class App(models.Model):
    """
    Model for storing application names
    """

    name = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = 'app'

    def __str__(self):
        return self.name
