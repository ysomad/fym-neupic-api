from rest_framework import serializers

from .models import Task, AppFunction, TaskData, Subfunction


class FunctionSerializer(serializers.ModelSerializer):
    app = serializers.StringRelatedField()

    class Meta:
        model = AppFunction
        fields = ('app', 'name')


class TaskDataSerializer(serializers.ModelSerializer):
    media_url = serializers.SerializerMethodField()
    function = FunctionSerializer(read_only=True)
    subfunction = serializers.StringRelatedField()
    
    class Meta:
        model = TaskData
        fields = ('media_url', 'function', 'subfunction')

    def get_media_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.media.url)


class TaskSerializer(serializers.ModelSerializer):
    data = TaskDataSerializer(read_only=True)
    bot = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ('id', 'data', 'bot', 'status')




