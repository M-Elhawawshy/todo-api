from rest_framework import serializers

from tasks.models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'is_completed', 'updated_at', 'created_at']
        read_only_fields = ['id', 'updated_at', 'created_at']