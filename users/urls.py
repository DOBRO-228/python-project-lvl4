from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.ListView.as_view(), name='list'),
    path('create/', views.RegistrationView.as_view(), name='register_user'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update_user'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
]
