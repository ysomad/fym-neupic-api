from rest_framework.serializers import StringRelatedField, ModelSerializer

from tasks.models import AppFunction, Task, Media, App, Bot, Subfunction


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'media', 'state', 'tags')


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'media', 'function', 'subfunction', 'bot', 'status')


class AppSerializer(ModelSerializer):
    class Meta:
        model = App
        fields = ('name',)


class SubfunctionSerializer(ModelSerializer):
    class Meta:
        model = Subfunction
        fields = ('id', 'name')


class AppFunctionSerializer(ModelSerializer):
    app = StringRelatedField()

    class Meta:
        model = AppFunction
        fields = ('id', 'name', 'app')


class BotSerializer(ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id', 'name', 'state')


class SubfunctionSerializer(ModelSerializer):
    function = AppFunctionSerializer(read_only=True)

    class Meta:
        model = Subfunction
        fields = ('id', 'name', 'function')


class TaskListSerializer(ModelSerializer):
    media = MediaSerializer(read_only=True)
    function =  StringRelatedField()
    subfunction = StringRelatedField()
    bot = StringRelatedField()

    class Meta:
        model = Task
        fields = ('id', 'status', 'media', 'function', 'subfunction', 'bot')


class TaskDetailSerializer(ModelSerializer):
    media = MediaSerializer(read_only=True)
    function =  AppFunctionSerializer(read_only=True)
    subfunction = SubfunctionSerializer(read_only=True)
    bot = BotSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'status', 'media', 'function', 'subfunction', 'bot')