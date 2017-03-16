# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from projects.models import Project
from users.models import UserProfile


# 设备类型
class EquipmentType(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'设备类型名称', default='')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备类型信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 设备信息
class Equipment(models.Model):
    equi_type = models.ForeignKey(EquipmentType, verbose_name=u'设备类型')
    equi_person = models.ForeignKey(UserProfile, verbose_name=u'设备负责人')

    equi_name = models.CharField(max_length=20, verbose_name=u'设备名称')
    equi_num = models.CharField(max_length=20, verbose_name=u'设备型号')
    equi_status = models.CharField(default='0', max_length=10, choices=(
        ('0', u'正常'),
        ('1', u'限制使用'),
        ('2', u'停用'),
    ), verbose_name=u'设备状态')
    effect_date = models.DateField(default=datetime.now, verbose_name=u'计量有效期')
    equi_money = models.CharField(max_length=10, verbose_name=u'购买价格')
    buy_date = models.DateField(default=datetime.now, verbose_name=u'购买日期')

    person = models.CharField(default=u'仓库', max_length=20, verbose_name=u'保管人')
    department = models.CharField(default=u'仓库', max_length=20, verbose_name=u'所在部门')
    use_date = models.DateField(default=datetime.now, verbose_name=u'领用时间')
    revert_date = models.DateField(default=datetime.now, verbose_name=u'归还时间')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equi_name


# 设备变更记录
class EquipmentChange(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name='设备名称')
    equi_type = models.CharField(max_length=20, verbose_name=u'设备类型')
    equi_person = models.CharField(max_length=20, verbose_name=u'设备负责人')

    equi_num = models.CharField(max_length=20, verbose_name=u'设备型号')
    equi_status = models.CharField(default='0', max_length=10, choices=(
        ('0', u'正常'),
        ('1', u'限制使用'),
        ('2', u'停用'),
    ), verbose_name=u'设备状态')
    effect_date = models.DateField(default=datetime.now, verbose_name=u'计量有效期')
    equi_money = models.CharField(max_length=10, verbose_name=u'购买价格')
    buy_date = models.DateField(default=datetime.now, verbose_name=u'购买日期')

    person = models.CharField(default=u'仓库', max_length=20, verbose_name=u'保管人')
    department = models.CharField(default=u'仓库', max_length=20, verbose_name=u'所在部门')
    use_date = models.DateField(default=datetime.now, verbose_name=u'领用时间')
    revert_date = models.DateField(default=datetime.now, verbose_name=u'归还时间')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备变更记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equipment
