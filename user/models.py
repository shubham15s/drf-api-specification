from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault(
            "username", email.split("@")[0]
        ) 
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    bio = models.TextField(blank=True, null=True)
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, null=True, related_name="users"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name", "date_of_birth"]

    objects = UserManager()


class LogEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="logs"
    )
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["user"]),  # Optimize queries filtering by user
            models.Index(fields=["action"]),  # Optimize queries filtering by action
            models.Index(
                fields=["timestamp"]
            ),  # Optimize queries filtering by timestamp
            models.Index(
                fields=["user", "action", "timestamp"]
            ),  # Optimize complex filters
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
