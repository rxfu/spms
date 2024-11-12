# Generated by Django 5.1.3 on 2024-11-12 10:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        ("settings", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
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
                ("year", models.CharField(max_length=4, verbose_name="评审年度")),
                (
                    "opinion",
                    models.TextField(blank=True, null=True, verbose_name="评审意见"),
                ),
                (
                    "is_agreed",
                    models.BooleanField(
                        blank=True, null=True, verbose_name="是否同意立项"
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="review_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者",
                    ),
                ),
                (
                    "panelist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="review_panelist",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="评审专家",
                    ),
                ),
                (
                    "phase",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="settings.phase",
                        verbose_name="项目阶段",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="projects.information",
                        verbose_name="评审项目",
                    ),
                ),
                (
                    "updator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="review_updator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="更新者",
                    ),
                ),
            ],
            options={
                "verbose_name": "项目评审",
                "verbose_name_plural": "项目评审",
            },
        ),
    ]