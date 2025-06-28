from django.contrib import admin
from django.urls import path

from tasks import views

urlpatterns = [
    path('', views.TasksCreateRetrieveAPIView.as_view()),
    path('<uuid:task_id>/', views.TasksRetrieveUpdateDestroyAPIView.as_view()),
]
