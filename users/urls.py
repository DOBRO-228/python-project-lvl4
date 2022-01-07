from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    path('', views.ListUserView.as_view(), name='list'),
    path('create/', views.RegisterUserView.as_view(), name='register'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete'),
]
