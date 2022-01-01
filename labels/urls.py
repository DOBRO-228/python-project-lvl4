from django.urls import path
from labels import views

app_name = 'labels'
urlpatterns = [
    path('', views.LabelListView.as_view(), name='list'),
    path('create/', views.CreateLabelView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateLabelView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete'),
]
