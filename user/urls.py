from django.urls import path
from . import views
app_name = "user"

urlpatterns = [
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_password/', views.user_password, name='user_password'),
    path('user_profile_view/', views.user_profile_view, name='user_profile_view'),
    path('user_profile_create/', views.user_profile_create, name='user_profile_create'),
    path('user_profile_update/<int:pk>', views.UserProfileUpdate.as_view(), name='user_profile_update'),
]