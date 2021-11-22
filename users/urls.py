from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.ListView.as_view(), name='list'),
    path('create/', views.register_user, name='register_user'),
    path('<int:pk>/update/', views.update_user, name='update_user'),
    path('<int:pk>/delete/', views.delete_user, name='delete_user'),
]
