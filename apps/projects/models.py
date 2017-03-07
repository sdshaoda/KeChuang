# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile


class Project(models.Model):
    pro_person = models.ForeignKey(UserProfile, verbose_name=u'项目负责人')
    pro_name = models.CharField(max_length=50, verbose_name=u'工程名称')
    ht_name = models.CharField(max_length=50, verbose_name=u'合同名称')
    ht_num = models.CharField(max_length=50, verbose_name=u'合同编号')
    ht_money = models.CharField(max_length=20, verbose_name=u'合同金额')
    wt_dw = models.CharField(max_length=50, verbose_name=u'委托单位')
    wt_person = models.CharField(max_length=20, verbose_name=u'委托人')
    mobile = models.CharField(max_length=20, verbose_name=u'联系电话')
    pro_address = models.CharField(max_length=50, verbose_name=u'项目地址')
    represent_person = models.CharField(max_length=20, verbose_name=u'公司代表')
    sign_date = models.DateField(default=datetime.now, max_length=20, verbose_name=u'签订日期')
    start_date = models.DateField(default=datetime.now, max_length=20, verbose_name=u'开工日期')
    finish_date = models.DateField(default=datetime.now, max_length=20, verbose_name=u'完工日期')
    pro_type = models.CharField(default='jkjc', max_length=4, choices=(
        ('jkjc', u'基坑监测'), ('jcgc', u'沉降观测'), ('zjjc', u'桩基检测'), ('clsy', u'材料试验'), ('gcwt', u'工程物探')
    ), verbose_name=u'工程类型')
    equipment = models.CharField(max_length=20, verbose_name=u'检测设备')
    ht_scan = models.FileField(upload_to='hetong/%Y/%m', verbose_name=u'合同扫描件', max_length=100)
    apply_person = models.CharField(max_length=20, default='', verbose_name=u'项目申请人')
    apply_type = models.CharField(default='0', max_length=2, choices=(
        ('0', u'审核通过'), ('1', u'申请添加'), ('2', u'申请修改'), ('3', u'申请删除')
    ), verbose_name=u'工程审核')
    apply_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name
