# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from equipments.models import Equipment
from projects.models import Project
from users.models import UserProfile


# 工程人员
class ProjectMember(models.Model):
    pro_name = models.ForeignKey(Project, verbose_name=u'工程名称')
    member = models.ForeignKey(UserProfile, verbose_name=u'项目成员')
    remark = models.CharField(max_length=200, verbose_name=u'备注', default='')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'项目成员信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name


# 工程设备，保存工程和设备的关联信息
class ProjectEquipment(models.Model):
    pro_name = models.ForeignKey(Project, verbose_name=u'工程名称')
    equipment = models.ForeignKey(Equipment, verbose_name=u'检测设备')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name


# 工程申请
class ProjectApply(models.Model):
    pro_name = models.ForeignKey(Project, verbose_name=u'工程名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'申请人')
    type = models.CharField(default='0', max_length=2, choices=(
        ('0', u'新增'), ('1', u'修改'), ('1', u'删除')
    ), verbose_name=u'申请类型')
    remark = models.CharField(max_length=200, verbose_name=u'备注', default='')
    status = models.CharField(default='0', max_length=2, choices=(
        ('0', u'部门主任审核中'), ('1', u'公司领导审核中'), ('2', u'审核通过'), ('3', u'审核未通过')
    ), verbose_name=u'工程审核状态')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')

    class Meta:
        verbose_name = u'工程申请信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name


# 设备申请
class EquipmentApply(models.Model):
    equi_name = models.ForeignKey(Equipment, verbose_name=u'设备名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'申请人')
    type = models.CharField(default='0', max_length=2, choices=(
        ('0', u'领用'), ('1', u'归还')
    ), verbose_name=u'申请类型')
    remark = models.CharField(max_length=200, verbose_name=u'备注', default='')
    status = models.CharField(default='0', max_length=2, choices=(
        ('0', u'审核中'), ('1', u'审核通过'), ('2', u'审核未通过')
    ), verbose_name=u'设备审核状态')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')

    class Meta:
        verbose_name = u'设备申请信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equi_name
