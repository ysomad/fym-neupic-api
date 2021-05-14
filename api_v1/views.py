from django.db.models import query
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView
)
from rest_framework.viewsets import ViewSet, ModelViewSet

from tasks.models import AppFunction, Media, Subfunction, Task
from .serializers import (
    AppFunctionSerializer, MediaSerializer, TaskSerializer, 
    TaskNestedSerializer, SubfunctionSerializer
)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskNestedSerializer
   
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

 