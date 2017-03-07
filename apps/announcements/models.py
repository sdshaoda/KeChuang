# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile


class Announcement(models.Model):
    person = models.ForeignKey(UserProfile, verbose_name=u'发布人')
    title = models.CharField(max_length=50, verbose_name=u'公告标题')
    content = models.TextField(verbose_name=u'公告正文')
    department = models.CharField(default='qgs', max_length=20, choices=(
        ("qgs", u"全公司"), ("zhb", u"综合办"), ("zgb", u"总工办"), ("jc1s", u"检测一室"),
        ("jc2s", u"检测二室"), ("jc3s", u"检测三室"), ("jc4s", u"检测四室"),
        ("tlsys", u"土力学实验室"), ("ytlxsys", u"岩土力学实验室"),
        ("gjgs", u"钢结构室"), ("sbyfs", u"设备研发室")
    ), verbose_name=u'相关部门')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'公告信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class Document(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'公文名称')
    document = models.FileField(upload_to='document/%Y/%m', verbose_name=u'公文')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'公文信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
