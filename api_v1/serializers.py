from rest_framework.serializers import (
    StringRelatedField, ModelSerializer, ListField
)
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer
)

from tasks.models import (
    AppFunction, Task, Media, App, Bot, Subfunction
)


class ListTagListSerializerField(TagListSerializerField, ListField):
    pass


class MediaSerializer(TaggitSerializer, ModelSerializer):
    tags = ListTagListSerializerField()

    class Meta:
        model = Media
        fields = ('id', 'media', 'type', 'tags')


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'media', 'function', 'subfunction', 'bot', 'status')


class AppSerializer(ModelSerializer):
    class Meta:
        model = App
        fields = ('id', 'name')


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


class TaskDetailSerializer(TaskSerializer, ModelSerializer):
    media = MediaSerializer(read_only=True, many=True)
    function = AppFunctionSerializer(read_only=True)
    subfunction = SubfunctionSerializer(read_only=True)
    bot = BotSerializer(read_only=True)

