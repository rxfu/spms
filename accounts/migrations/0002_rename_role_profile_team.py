# Generated by Django 5.1.3 on 2024-12-01 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="role",
            new_name="team",
        ),
    ]