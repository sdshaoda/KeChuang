# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile
from projects.models import Project


class Equipment(models.Model):
    equi_person = models.ForeignKey(UserProfile, verbose_name=u'设备负责人')
    equi_name = models.CharField(max_length=20, verbose_name=u'设备名称')
    equi_num = models.CharField(max_length=20, verbose_name=u'设备型号')
    equi_type = models.CharField(default='0', max_length=20, choices=(
        ('0', u'检测设备'), ('1', u'监测设备'), ('2', u'物探设备'), ('3', u'材料试验'),
    ), verbose_name=u'设备分类')
    equi_status = models.CharField(default='normal', max_length=10, choices=(
        ('normal', u'正常'),
        ('Restricted', u'限制使用'),
        ('useless', u'停用'),
    ), verbose_name=u'设备状态')
    effect_date = models.DateField(default=datetime.now, verbose_name=u'计量有效期')
    equi_money = models.CharField(max_length=10, verbose_name=u'购买价格')
    buy_date = models.DateField(default=datetime.now, verbose_name=u'购买日期')
    person = models.CharField(default=u'仓库', max_length=20, verbose_name=u'保管人')
    department = models.CharField(default='jcys', max_length=20, choices=(
        ("zhb", u"综合办"), ("zgb", u"总工办"), ("jc1s", u"检测一室"),
        ("jc2s", u"检测二室"), ("jc3s", u"检测三室"), ("jc4s", u"检测四室"),
        ("tlsys", u"土力学实验室"), ("ytlxsys", u"岩土力学实验室"),
        ("gjgs", u"钢结构室"), ("sbyfs", u"设备研发室")
    ), verbose_name=u'所在部门')
    use_date = models.DateField(default=datetime.now, verbose_name=u'领用时间')
    revert_data = models.DateField(default=datetime.now, verbose_name=u'归还时间')
    relate_project = models.CharField(max_length=50, verbose_name=u'挂靠项目')
    remark = models.CharField(max_length=200, verbose_name=u'使用维修说明')
    apply_person = models.CharField(max_length=20, default='', verbose_name=u'设备申请人')
    apply_type = models.CharField(default='0', max_length=2, choices=(
        ('0', u'审核通过'), ('1', u'申请领用'), ('2', u'申请归还')
    ), verbose_name=u'设备审核')
    apply_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equi_name
