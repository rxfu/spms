# Generated by Django 5.1.3 on 2024-11-29 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0002_setting_is_opend"),
    ]

    operations = [
        migrations.RenameField(
            model_name="setting",
            old_name="is_opend",
            new_name="is_opened",
        ),
    ]