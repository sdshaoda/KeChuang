# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile, Department


# 公告信息
class Announcement(models.Model):
    person = models.ForeignKey(UserProfile, verbose_name=u'发布人')
    department = models.ForeignKey(Department, verbose_name=u'相关部门')

    title = models.CharField(max_length=50, verbose_name=u'公告标题')
    content = models.TextField(verbose_name=u'公告正文')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'公告信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


# 公文信息
class Document(models.Model):
    person = models.ForeignKey(UserProfile, verbose_name=u'上传人')
    department = models.ForeignKey(Department, verbose_name=u'相关部门')

    name = models.CharField(max_length=20, verbose_name=u'公文名称')
    document = models.FileField(upload_to='document/%Y/%m', verbose_name=u'公文')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'公文信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
