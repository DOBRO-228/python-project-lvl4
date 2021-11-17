from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('create', views.IndexView.as_view(), name='create_user'),
    # path('<int:pk>/update/', views.DetailView.as_view(), name='create_user'),
]
