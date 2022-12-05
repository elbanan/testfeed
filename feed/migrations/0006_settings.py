# Generated by Django 4.1.1 on 2022-12-01 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feed", "0005_delete_settings"),
    ]

    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("frequency", models.IntegerField(default=1)),
                (
                    "day_of_week",
                    models.IntegerField(
                        choices=[
                            ("1", "Monday"),
                            ("2", "Tuesday"),
                            ("3", "Wednesday"),
                            ("4", "Thursday"),
                            ("5", "Friday"),
                            ("6", "Saturday"),
                            ("7", "Sunday"),
                        ],
                        default=1,
                    ),
                ),
                ("keywords", models.CharField(max_length=1000, null=True)),
                ("bookmarks", models.ManyToManyField(to="feed.article")),
                ("subscription", models.ManyToManyField(to="feed.journal")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]