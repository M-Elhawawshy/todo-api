from functools import partial

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from tasks.models import TasksUser, Tasks
from tasks.serializers import TasksSerializer


class TasksCreateRetrieveAPIView(generics.ListCreateAPIView):
    serializer_class = TasksSerializer
    queryset = Tasks.objects.all()

    def post(self, request, *args, **kwargs):
        serializer: TasksSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        title = data['title']
        description = data['description']

        try:
            tasks_user = TasksUser.objects.get(id=request.user_id)
        except TasksUser.DoesNotExist:
            return Response("missing user_id in request", status=status.HTTP_401_UNAUTHORIZED)

        task = Tasks.objects.create(
            owner=tasks_user,
            title=title,
            description=description,
        )

        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TasksRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TasksSerializer

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('task_id')

        try:
            task = Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            return Response("task does not exist", status=status.HTTP_400_BAD_REQUEST)

        if str(task.owner.id) != request.user_id:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        serializer: TasksSerializer = self.get_serializer(task)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        id = kwargs.get('task_id')

        try:
            task = Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            return Response("task does not exist", status=status.HTTP_400_BAD_REQUEST)

        if str(task.owner.id) != request.user_id:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        serializer: TasksSerializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('task_id')

        try:
            task = Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            return Response("task does not exist", status=status.HTTP_400_BAD_REQUEST)

        if str(task.owner.id) != request.user_id:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)