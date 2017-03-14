# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile


# 工程类型
class ProjectType(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'工程类型名称')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程类型信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 项目阶段
class ProjectStage(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'项目阶段名称')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'项目阶段信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 工程信息
class Project(models.Model):
    pro_type = models.ForeignKey(ProjectType, verbose_name=u'工程类型')
    pro_person = models.ForeignKey(UserProfile, verbose_name=u'项目负责人')
    wt_person = models.ForeignKey(UserProfile, verbose_name=u'法人委托', null=True, blank=True)
    ht_person = models.ForeignKey(UserProfile, verbose_name=u'合同签署人', null=True, blank=True)
    stage = models.ForeignKey(ProjectStage, verbose_name=u'项目阶段', null=True, blank=True)

    pro_name = models.CharField(max_length=50, verbose_name=u'工程名称')
    ht_name = models.CharField(max_length=50, verbose_name=u'合同名称', null=True, blank=True)
    ht_num = models.CharField(max_length=50, verbose_name=u'合同编号', null=True, blank=True)
    ht_money = models.CharField(max_length=20, verbose_name=u'合同金额', null=True, blank=True)
    js_money = models.CharField(max_length=20, verbose_name=u'结算金额', null=True, blank=True)
    wt_dw = models.CharField(max_length=50, verbose_name=u'委托单位', null=True, blank=True)
    mobile = models.CharField(max_length=20, verbose_name=u'联系电话', null=True, blank=True)
    pro_address = models.CharField(max_length=50, verbose_name=u'项目地址', null=True, blank=True)
    sign_date = models.DateField(default=datetime.now, max_length=20, verbose_name=u'签订日期', null=True, blank=True)
    start_date = models.DateField(default=datetime.now, max_length=20, verbose_name=u'开工日期', null=True, blank=True)
    finish_date = models.DateField(default=datetime.now, max_length=20, verbose_name=u'完工日期', null=True, blank=True)
    # pro_type = models.CharField(default='jkjc', max_length=4, choices=(
    #     ('jkjc', u'基坑监测'), ('jcgc', u'沉降观测'), ('zjjc', u'桩基检测'), ('clsy', u'材料试验'), ('gcwt', u'工程物探')
    # ), verbose_name=u'工程类型')
    ht_scan = models.FileField(upload_to='hetong/%Y/%m', verbose_name=u'合同扫描件', max_length=100, null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name
