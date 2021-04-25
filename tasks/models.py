from django.db import models


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = 'new'
        PROCESSING = 'processing'
        FINISHED = 'finished'

    data = models.ForeignKey(
        'TaskData', 
        on_delete=models.CASCADE
    )
    bot = models.ForeignKey(
        'Bot', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE
    ) 
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task'

    def __str__(self):
       return str(self.created_at)


class TaskData(models.Model):
    media = models.ImageField(upload_to='tasks')
    function = models.ForeignKey(
        'AppFunction', verbose_name='function', on_delete=models.CASCADE)
    subfunction = models.ForeignKey(
        'Subfunction', 
        null=True,
        blank=True,
        verbose_name='subfunction', 
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'task_data'

    def __str__(self):
        return f'{self.function.app} - {self.function}'


class AppFunction(models.Model):
    name = models.CharField(max_length=32, unique=True)
    app = models.ForeignKey(
        'App', 
        verbose_name='app', 
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'app_function'

    def __str__(self):
        return self.name


class Subfunction(models.Model):
    name = models.CharField(max_length=32, unique=True)

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
        max_length=16, choices=State.choices, default=State.DISABLED)

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
