# Generated by Django 4.1.1 on 2022-12-01 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0003_settings_keywords_alter_settings_day_of_week_votes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="settings",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]