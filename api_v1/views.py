from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView
)
from rest_framework.viewsets import ModelViewSet

from drf_yasg.utils import swagger_auto_schema

from tasks.models import AppFunction, Media, Subfunction, Task
from .serializers import (
    AppFunctionSerializer, MediaSerializer, TaskSerializer, 
    TaskDetailSerializer, SubfunctionSerializer
)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(responses={200: TaskDetailSerializer})
    def retrieve(self, request, pk):
        instance = self.get_object()
        serializer = TaskDetailSerializer(instance)
        return Response(serializer.data)


class MediaList(ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class MediaDetail(RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class AppFunctionList(ListAPIView):
    queryset = AppFunction.objects.all()
    serializer_class = AppFunctionSerializer


class SubfunctionList(ListAPIView):
    queryset = Subfunction.objects.all()
    serializer_class = SubfunctionSerializer

 