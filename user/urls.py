from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    LoginView,
    LogoutView,
    UserProfileUpdateView,
    FetchUserDetailsView,
    UserLogsView,
    FilterLogsView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/update/", UserProfileUpdateView.as_view(), name="profile_update"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("details/", FetchUserDetailsView.as_view(), name="fetch_users"),
    path("logs/<int:user_id>/", UserLogsView.as_view(), name="user_logs"),
    path("logs/filter/", FilterLogsView.as_view(), name="filter_logs"),
]
