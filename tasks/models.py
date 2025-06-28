import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


# Create your models here.
class TasksUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(TasksUser, on_delete=CASCADE)
    title = models.TextField(max_length=50, null=False)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)