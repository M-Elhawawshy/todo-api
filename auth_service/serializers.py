from rest_framework import serializers

from tasks.models import TasksUser


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksUser  # or your custom user model
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        if TasksUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if TasksUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        return TasksUser.objects.create_user(**validated_data)


class RefreshSerializer(serializers.Serializer):
    pass

class LogoutSerializer(serializers.Serializer):
    pass