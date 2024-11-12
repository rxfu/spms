from django.contrib.auth.models import User
from django.db import models

import settings.models as settings


# Create your models here.
class Role(models.Model):
    name = models.CharField("名称", max_length=150)

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, verbose_name='角色')
    name = models.CharField("姓名", null=True, blank=True, max_length=150)
    gender = models.ForeignKey(settings.Gender, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='profile_gender', verbose_name='性别')
    phone = models.CharField("联系电话", null=True, blank=True, max_length=11)
    idtype = models.ForeignKey(settings.Idtype, on_delete=models.DO_NOTHING, related_name='profile_idtype',
                               verbose_name="证件类型", null=True)
    idnumber = models.CharField("证件号码", null=True, blank=True, unique=True, max_length=18)
    college = models.CharField('所在院校', null=True, blank=True, max_length=200)
    department = models.ForeignKey(settings.Department, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='profile_department',
                                   verbose_name="所属单位")
    education = models.ForeignKey(settings.Education, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name='profile_education', verbose_name="最高学历")
    degree = models.ForeignKey(settings.Degree, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='profile_degree', verbose_name="最高学位")
    title = models.ForeignKey(settings.Title, on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name='profile_title', verbose_name="职称")
    subject = models.ForeignKey(settings.Subject, on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='profile_subject', verbose_name="所在学科")
    area = models.CharField("研究领域", null=True, blank=True, max_length=150)
    account = models.CharField('银行卡号', unique=True, null=True, blank=True, max_length=20)
    bank = models.CharField('开户行信息', null=True, blank=True, max_length=200)
    bankno = models.CharField('开户行行联号', null=True, blank=True, max_length=12)
    is_enable = models.BooleanField("是否启用", default=True)
    remark = models.TextField('备注', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='profile_creator',
                                verbose_name="创建者")
    updator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='profile_updator',
                                verbose_name="更新者")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
