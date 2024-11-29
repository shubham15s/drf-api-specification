from rest_framework import serializers
from .models import User, State, LogEntry


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "date_of_birth", "bio", "state"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "date_of_birth", "bio", "state"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "date_of_birth", "bio", "state"]


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ["id", "user", "action", "timestamp", "ip_address", "description"]
