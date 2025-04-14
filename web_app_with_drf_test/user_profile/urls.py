from django.urls import path
from .views import GetUserProfile, update_user_profile


urlpatterns = [
    path('get_user_profile/', GetUserProfile.as_view(), ),
    path('update_profile/<int:pk>/', update_user_profile, name='update_user_profile'),


]
