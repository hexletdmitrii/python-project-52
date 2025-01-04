from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path('users/', views.UserListView.as_view(), name='users_list'),
    path('users/create/', views.UserCreateView.as_view(), name='add_user'),
    path('login/', views.LoginUserView.as_view(), name='users_login'),
    path('logout/', views.UserLogoutView.as_view(), name='users_logout'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete_user'),
]
