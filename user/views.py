from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, LogEntry
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserProfileUpdateSerializer,
    LogEntrySerializer,
)
from django.utils.timezone import now, timedelta


def create_log(user, action, description):
    LogEntry.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address="127.0.0.1"  
    )


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data.get("email"))
            create_log(user, "LOGIN", "User logged in successfully.")
        response.data["message"] = "Login successful."
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Revoke the refresh token
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            create_log(request.user, "LOGOUT", "User logged out successfully.")
            return Response({"message": "Logout successful."}, status=200)

        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Profile updated successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class FetchUserDetailsView(APIView):
    def get(self, request):
        # Use the 'read' database for querying
        users = User.objects.using("read").all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})


class UserLogsView(APIView):
    def get(self, request, user_id):
        """
        Retrieve all logs for a specific user.
        """
        logs = LogEntry.objects.filter(user_id=user_id).order_by("-timestamp")
        serializer = LogEntrySerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterLogsView(APIView):
    def get(self, request):
        """
        Filter logs by action and timestamp.
        Query Parameters:
          - action (required): The action to filter logs by.
          - days (optional): The number of days to look back. Default is 7 days.
        """
        action = request.query_params.get("action")
        days = int(request.query_params.get("days", 7))

        if not action:
            return Response(
                {"error": "Action query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_date = now() - timedelta(days=days)
        logs = LogEntry.objects.filter(
            action=action, timestamp__gte=start_date
        ).order_by("-timestamp")
        serializer = LogEntrySerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
