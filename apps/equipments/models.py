# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime,date

from django.db import models

from projects.models import Project


# 设备类型
class EquipmentType(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'设备类型名称')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    # 类型下的所有设备
    def get_equipments(self):
        return self.equipment_set.filter(id=self.id)

    class Meta:
        verbose_name = u'设备类型信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 设备基本信息
class Equipment(models.Model):
    equ_type = models.ForeignKey(EquipmentType, verbose_name=u'设备类型', null=True, blank=True)

    # 设备基本信息
    equ_name = models.CharField(max_length=20, verbose_name=u'设备名称')
    equ_person_id = models.IntegerField(verbose_name=u'设备负责人id', null=True, blank=True)
    file_num = models.CharField(max_length=20, verbose_name=u'档案编号')
    equ_num = models.CharField(max_length=20, verbose_name=u'设备型号')
    equ_status = models.CharField(default='0', max_length=10, choices=(
        ('0', u'正常'),
        ('1', u'限制使用'),
        ('2', u'停用'),
    ), verbose_name=u'设备状态')
    effect_date = models.DateField(default=date.today, verbose_name=u'计量有效期')
    equ_money = models.CharField(max_length=10, verbose_name=u'购买价格')
    buy_date = models.DateField(default=date.today, verbose_name=u'购买日期')

    # 设备领用信息
    use_status = models.CharField(default='0', max_length=10, choices=(
        ('0', u'未领用'),
        ('1', u'已领用'),
    ), verbose_name=u'使用状态')
    equ_staff_id = models.IntegerField(verbose_name=u'设备保管人id', null=True, blank=True)
    use_date = models.DateField(verbose_name=u'领用时间', null=True, blank=True)
    revert_date = models.DateField(verbose_name=u'归还时间', null=True, blank=True)

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    # 设备负责人
    def get_person(self):
        return self.equipmentperson_set.get(equipment_id=self.id)

    # 设备保管人
    def get_staff(self):
        return self.equipmentstaff_set.get(equipment_id=self.id)

    # 正在审核中的 设备申请
    def get_applys(self):
        return self.equipmentapply_set.filter(equipment_id=self.id, status='0')

    class Meta:
        verbose_name = u'设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equ_name

# 设备变更记录
# class EquipmentChange(models.Model):
#     equipment = models.ForeignKey(Equipment, verbose_name='设备名称')
#
#     equi_type = models.CharField(max_length=20, verbose_name=u'设备类型')
#     equi_person = models.CharField(max_length=20, verbose_name=u'设备负责人')
#     equi_num = models.CharField(max_length=20, verbose_name=u'设备型号')
#     equi_status = models.CharField(default='0', max_length=10, choices=(
#         ('0', u'正常'),
#         ('1', u'限制使用'),
#         ('2', u'停用'),
#     ), verbose_name=u'设备状态')
#     effect_date = models.DateField(default=datetime.now, verbose_name=u'计量有效期')
#     equi_money = models.CharField(max_length=10, verbose_name=u'购买价格')
#     buy_date = models.DateField(default=datetime.now, verbose_name=u'购买日期')
#     remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)
#
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#
#     class Meta:
#         verbose_name = u'设备变更记录'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.equipment
