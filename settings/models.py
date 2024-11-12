from django.contrib.auth.models import User
from django.db import models
from django.db.models import DO_NOTHING


# Create your models here.
class Gender(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "性别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Idtype(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "身份证件类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Education(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "学历"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "学位"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "职称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "学科"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = "研究类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField('名称', max_length=100)
    is_enable = models.BooleanField("是否启用", default=True)
    order = models.IntegerField("排序", default=0)

    class Meta:
        verbose_name = '单位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField("名称", max_length=255)
    is_enable = models.BooleanField("是否启用", default=True)

    class Meta:
        verbose_name = "项目系列"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Phase(models.Model):
    name = models.CharField("名称", max_length=60)

    class Meta:
        verbose_name = '项目阶段'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Setting(models.Model):
    year = models.CharField('年度', max_length=4)
    series = models.ForeignKey(Series, on_delete=models.DO_NOTHING, verbose_name='项目系列')
    phase = models.ForeignKey(Phase, on_delete=DO_NOTHING, null=True, blank=True, verbose_name='项目阶段')
    submit_beg_time = models.DateTimeField('开始提交时间', null=True, blank=True)
    submit_end_time = models.DateTimeField('结束提交时间', null=True, blank=True)
    review_beg_time = models.DateTimeField('开始评审时间', null=True, blank=True)
    review_end_time = models.DateTimeField('结束评审时间', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='setting_creator',
                                verbose_name="创建者")
    updator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='setting_updator',
                                verbose_name="更新者")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = "项目设置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.year + '年度' + self.series.name
