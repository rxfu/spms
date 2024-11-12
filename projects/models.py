from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

import settings.models as settings


# Create your models here.
class Member(models.Model):
    name = models.CharField("姓名", null=True, blank=True, max_length=150)
    gender = models.ForeignKey(settings.Gender, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='member_gender', verbose_name='性别')
    phone = models.CharField("联系电话", null=True, blank=True, max_length=11)
    department = models.ForeignKey(settings.Department, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='member_department',
                                   verbose_name="所属单位")
    education = models.ForeignKey(settings.Education, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name='member_education', verbose_name="最高学历")
    degree = models.ForeignKey(settings.Degree, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='member_degree', verbose_name="最高学位")
    title = models.ForeignKey(settings.Title, on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name='member_title', verbose_name="职称")
    subject = models.ForeignKey(settings.Subject, on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='member_subject', verbose_name="所在学科")
    area = models.CharField("研究领域", null=True, blank=True, max_length=150)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='member_creator', verbose_name="创建者")
    updator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='member_updator', verbose_name="更新者")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = verbose_name


class Information(models.Model):
    year = models.CharField('申报年度', max_length=4)
    name = models.CharField('项目名称', null=True, blank=True, max_length=200)
    beg_year = models.CharField('起始年份', null=True, blank=True, max_length=4)
    end_year = models.CharField('结束年份', null=True, blank=True, max_length=4)
    type = models.ForeignKey(settings.Type, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='研究类型')
    direction = models.CharField("研究方向", null=True, blank=True, max_length=200)
    subject = models.ForeignKey(settings.Subject, on_delete=models.DO_NOTHING, verbose_name="所属学科", null=True)
    members = models.ManyToManyField(Member, blank=True, verbose_name='项目组成员')
    purpose = models.TextField('研究的目的和意义', null=True, blank=True)
    content = models.TextField('研究内容', null=True, blank=True)
    progress = models.TextField('研究进度', null=True, blank=True)
    result = models.TextField('预期成果', null=True, blank=True)
    budget = models.TextField(' 经费预算', null=True, blank=True)
    opinion = models.TextField(' 审核意见', null=True, blank=True)
    application_attachment = models.FileField('项目申报附件', null=True, blank=True,
                                              validators=[
                                                  FileExtensionValidator(allowed_extensions=['doc', 'docx', "pdf"])])
    inspection_attachment = models.FileField('中期检查附件', null=True, blank=True,
                                             validators=[
                                                 FileExtensionValidator(allowed_extensions=['doc', 'docx', "pdf"])])
    conclusion_attachment = models.FileField('项目结题附件', null=True, blank=True,
                                             validators=[
                                                 FileExtensionValidator(allowed_extensions=['doc', 'docx', "pdf"])])
    applicant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='project_applicant',
                                  verbose_name='申请者')
    application_opinion = models.TextField('申报审核意见', null=True, blank=True)
    application_is_agreed = models.BooleanField('是否同意申报', null=True, blank=True)
    application_panelist = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                             related_name='project_application_panelist',
                                             verbose_name='项目申报评审专家')
    inspection_opinion = models.TextField('中期检查意见', null=True, blank=True)
    inspection_is_agreed = models.BooleanField('检查是否合格', null=True, blank=True)
    inspection_panelist = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                            related_name='project_inspection_panelist', verbose_name='中期检查评审专家')
    conclusion_opinion = models.TextField('结题审核意见', null=True, blank=True)
    conclusion_is_agreed = models.BooleanField('是否允许结题', null=True, blank=True)
    conclusion_panelist = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                            related_name='project_conclusion_panelist', verbose_name='项目结题评审专家')
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='project_creator',
                                verbose_name="创建者")
    updator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='project_updator',
                                verbose_name="更新者")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
