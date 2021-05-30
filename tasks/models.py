from django.db import models
from django.db.models.fields.related import ForeignKey

from taggit.managers import TaggableManager


class Media(models.Model):

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
    preview = models.CharField(max_length=2048, blank=True, null=True)
    type = models.CharField(max_length=16, choices=Type.choices)
    tags = TaggableManager(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'media'
        verbose_name_plural = 'media'

    def __str__(self):
        return str(self.media)


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'new'
        PROCESSING = 'processing'
        DONE = 'done'
        ERROR = 'error'

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
    name = models.CharField(max_length=32, unique=True)
    app = ForeignKey('App', on_delete=models.CASCADE)

    class Meta:
        db_table = 'app_function'

    def __str__(self):
        return self.name


class Subfunction(models.Model):
    name = models.CharField(max_length=32, unique=True)
    function = models.ForeignKey(
        'AppFunction', null=True, on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'subfunction'

    def __str__(self):
        return self.name


class Bot(models.Model):

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
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = 'app'

    def __str__(self):
        return self.name
