from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, ChangePasswordView, UpdateProfileView, VerifyTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),
]
