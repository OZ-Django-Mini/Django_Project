from django.urls import path
from .views import RegisterView , LogoutView , UserDetailUpdateView , UserDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserDetailUpdateView.as_view(), name='user_profile'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
]