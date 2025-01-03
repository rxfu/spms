# Generated by Django 5.1.3 on 2024-11-29 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_alter_information_budget"),
    ]

    operations = [
        migrations.AddField(
            model_name="information",
            name="department_is_agreed",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="学院是否同意申报"
            ),
        ),
        migrations.AlterField(
            model_name="information",
            name="opinion",
            field=models.TextField(blank=True, null=True, verbose_name=" 学院审核意见"),
        ),
    ]
