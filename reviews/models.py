from django.contrib.auth.models import User
from django.db import models

import settings.models as settings
from projects.models import Information


# Create your models here.
class Review(models.Model):
    year = models.CharField('评审年度', max_length=4)
    project = models.ForeignKey(Information, on_delete=models.DO_NOTHING, null=True, blank=True,
                                verbose_name='评审项目')
    phase = models.ForeignKey(settings.Phase, on_delete=models.DO_NOTHING, null=True, blank=True,
                              verbose_name='项目阶段')
    opinion = models.TextField('评审意见', null=True, blank=True)
    is_agreed = models.BooleanField('是否同意立项', null=True, blank=True)
    panelist = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='review_panelist',
                                 verbose_name='评审专家')
    is_confirmed = models.BooleanField('是否已经确认', default=False)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='review_creator', verbose_name="创建者")
    updator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='review_updator', verbose_name="更新者")
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '项目评审'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project.name
