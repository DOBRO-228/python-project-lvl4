from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.TasksListView.as_view(), name='list'),
    path('create/', views.CreateTaskView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete'),
]
