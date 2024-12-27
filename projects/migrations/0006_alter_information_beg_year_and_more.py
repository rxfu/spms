# Generated by Django 5.1.3 on 2024-12-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0005_alter_information_application_attachment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="information",
            name="beg_year",
            field=models.DateField(blank=True, null=True, verbose_name="起始年份"),
        ),
        migrations.AlterField(
            model_name="information",
            name="end_year",
            field=models.DateField(blank=True, null=True, verbose_name="结束年份"),
        ),
    ]