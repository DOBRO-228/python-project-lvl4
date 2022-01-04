from django.urls import path
from statuses import views

app_name = 'statuses'
urlpatterns = [
    path('', views.StatusListView.as_view(), name='list'),
    path('create/', views.CreateStatusView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateStatusView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteStatusView.as_view(), name='delete'),
]
