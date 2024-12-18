# Generated by Django 5.1.3 on 2024-11-29 11:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Degree",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "学位",
                "verbose_name_plural": "学位",
            },
        ),
        migrations.CreateModel(
            name="Department",
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
                ("name", models.CharField(max_length=100, verbose_name="名称")),
                (
                    "is_enable",
                    models.BooleanField(default=True, verbose_name="是否启用"),
                ),
                ("order", models.IntegerField(default=0, verbose_name="排序")),
            ],
            options={
                "verbose_name": "单位",
                "verbose_name_plural": "单位",
            },
        ),
        migrations.CreateModel(
            name="Education",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "学历",
                "verbose_name_plural": "学历",
            },
        ),
        migrations.CreateModel(
            name="Gender",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "性别",
                "verbose_name_plural": "性别",
            },
        ),
        migrations.CreateModel(
            name="Idtype",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "身份证件类型",
                "verbose_name_plural": "身份证件类型",
            },
        ),
        migrations.CreateModel(
            name="Phase",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "项目阶段",
                "verbose_name_plural": "项目阶段",
            },
        ),
        migrations.CreateModel(
            name="Series",
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
                ("name", models.CharField(max_length=255, verbose_name="名称")),
                (
                    "is_enable",
                    models.BooleanField(default=True, verbose_name="是否启用"),
                ),
            ],
            options={
                "verbose_name": "项目系列",
                "verbose_name_plural": "项目系列",
            },
        ),
        migrations.CreateModel(
            name="Subject",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "学科",
                "verbose_name_plural": "学科",
            },
        ),
        migrations.CreateModel(
            name="Title",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "职称",
                "verbose_name_plural": "职称",
            },
        ),
        migrations.CreateModel(
            name="Type",
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
                ("name", models.CharField(max_length=60, verbose_name="名称")),
            ],
            options={
                "verbose_name": "研究类型",
                "verbose_name_plural": "研究类型",
            },
        ),
        migrations.CreateModel(
            name="Setting",
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
                ("year", models.CharField(max_length=4, verbose_name="年度")),
                (
                    "submit_beg_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="开始提交时间"
                    ),
                ),
                (
                    "submit_end_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="结束提交时间"
                    ),
                ),
                (
                    "review_beg_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="开始评审时间"
                    ),
                ),
                (
                    "review_end_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="结束评审时间"
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
                        related_name="setting_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者",
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
                    "series",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="settings.series",
                        verbose_name="项目系列",
                    ),
                ),
                (
                    "updator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="setting_updator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="更新者",
                    ),
                ),
            ],
            options={
                "verbose_name": "项目设置",
                "verbose_name_plural": "项目设置",
            },
        ),
    ]
