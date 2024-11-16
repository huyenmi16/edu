from django.urls import path
from .views import RegisterUser, CustomAuthToken, ProfileDetail

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', ProfileDetail.as_view(), name='profile'),
]
