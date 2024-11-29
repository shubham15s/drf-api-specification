# Generated by Django 5.1.3 on 2024-11-26 04:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_alter_user_managers"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action", models.CharField(max_length=100)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("ip_address", models.GenericIPAddressField()),
                ("description", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["user"], name="user_logent_user_id_2da938_idx"
                    ),
                    models.Index(
                        fields=["action"], name="user_logent_action_79234c_idx"
                    ),
                    models.Index(
                        fields=["timestamp"], name="user_logent_timesta_038bbf_idx"
                    ),
                    models.Index(
                        fields=["user", "action", "timestamp"],
                        name="user_logent_user_id_f7ce44_idx",
                    ),
                ],
            },
        ),
    ]
