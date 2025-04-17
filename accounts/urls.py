from django.urls import path
from .views import RegisterApiView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterApiView.as_view(), ),
    path('login/', CustomTokenObtainPairView.as_view(), ),
    path('token-refresh/', TokenRefreshView.as_view(), ),


]
