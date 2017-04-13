# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime, date

from django.db import models


# 设备类型
class EquipmentType(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'设备类型名称')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备类型信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 设备基本信息
class Equipment(models.Model):
    equ_type = models.ForeignKey(EquipmentType, verbose_name=u'设备类型', null=True, blank=True)
    equ_type_name = models.CharField(max_length=20, verbose_name=u'设备类型名称', null=True, blank=True)

    # 设备基本信息
    equ_name = models.CharField(max_length=20, verbose_name=u'设备名称')
    equ_person_id = models.IntegerField(verbose_name=u'设备负责人id', null=True, blank=True)
    equ_person = models.CharField(max_length=20, verbose_name=u'设备负责人', null=True, blank=True)
    file_num = models.CharField(max_length=20, verbose_name=u'档案编号', null=True, blank=True)
    equ_num = models.CharField(max_length=20, verbose_name=u'设备型号', null=True, blank=True)
    equ_status = models.CharField(default=u'正常', max_length=10, choices=(
        (u'正常', u'正常'),
        (u'限制使用', u'限制使用'),
        (u'停用', u'停用'),
    ), verbose_name=u'设备状态')
    number = models.CharField(max_length=20, verbose_name=u'设备编号', null=True, blank=True)
    biaodingzs = models.CharField(max_length=20, verbose_name=u'标定证书号', null=True, blank=True)
    biaoding_date = models.DateField(verbose_name=u'标定日期', null=True, blank=True)
    effect_date = models.DateField(verbose_name=u'计量有效期', null=True, blank=True)
    equ_money = models.CharField(max_length=10, verbose_name=u'购买价格', null=True, blank=True)
    buy_date = models.DateField(verbose_name=u'购买日期', null=True, blank=True)

    # 设备领用信息
    use_status = models.CharField(default='未领用', max_length=10, choices=(
        ('未领用', u'未领用'),
        ('已领用', u'已领用'),
    ), verbose_name=u'使用状态')
    equ_staff_id = models.IntegerField(verbose_name=u'设备保管人id', null=True, blank=True)
    equ_staff = models.CharField(max_length=20, verbose_name=u'设备保管人', null=True, blank=True)
    department_id = models.IntegerField(verbose_name=u'所在部门id', null=True, blank=True)
    department = models.CharField(max_length=20, verbose_name=u'所在部门', null=True, blank=True)
    use_date = models.DateField(verbose_name=u'领用时间', null=True, blank=True)
    revert_date = models.DateField(verbose_name=u'归还时间', null=True, blank=True)

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equ_name
