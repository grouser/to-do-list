from django.urls import include, path
from todolist.tasks import api_urls
from . import api_views

urlpatterns = [
    path('', api_views.TaskListCreateAPIView.as_view(), name='task-list'),
    path('<int:pk>/', api_views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
]
