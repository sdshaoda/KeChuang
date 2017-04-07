# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime, date

from django.db import models

from equipments.models import Equipment
from projects.models import Project, ProjectChange
from users.models import UserProfile, Department


# 工程负责人
class ProjectPerson(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'负责人')

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程负责人信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 工程项目成员
class ProjectMember(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程名称')
    member = models.ForeignKey(UserProfile, verbose_name=u'项目成员')

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'项目成员信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 工程设备
class ProjectEquipment(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程名称')
    equipment = models.ForeignKey(Equipment, verbose_name=u'检测设备')

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 工程申请
class ProjectApply(models.Model):
    # 工程申请与 变更记录 相关
    project = models.ForeignKey(ProjectChange, verbose_name=u'工程名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'申请人')

    type = models.CharField(default='0', max_length=2, choices=(
        ('0', u'新增'), ('1', u'修改'), ('1', u'删除')
    ), verbose_name=u'申请类型')
    status = models.CharField(default='0', max_length=2, choices=(
        ('0', u'部门主任审核中'), ('1', u'公司领导审核中'), ('2', u'审核通过'), ('3', u'审核未通过')
    ), verbose_name=u'审核状态')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')

    class Meta:
        verbose_name = u'工程申请信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 设备负责人
class EquipmentPerson(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name=u'设备名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'负责人')

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备负责人信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equipment


# 设备保管人
class EquipmentStaff(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name=u'设备名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'保管人', null=True, blank=True)

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'设备保管人信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equipment


# 设备申请
class EquipmentApply(models.Model):
    # 设备申请信息
    equipment = models.ForeignKey(Equipment, verbose_name=u'设备名称')
    person = models.ForeignKey(UserProfile, verbose_name=u'申请人')

    equipment_person_id = models.CharField(max_length=10, verbose_name=u'设备负责人id')
    type = models.CharField(default='0', max_length=2, choices=(
        ('0', u'领用'), ('1', u'归还')
    ), verbose_name=u'申请类型')
    status = models.CharField(default='0', max_length=2, choices=(
        ('0', u'审核中'), ('1', u'审核通过'), ('2', u'审核未通过')
    ), verbose_name=u'审核状态')
    use_date = models.DateField(default=date.today, verbose_name=u'领用时间', null=True, blank=True)
    revert_date = models.DateField(default=date.today, verbose_name=u'归还时间', null=True, blank=True)
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')

    class Meta:
        verbose_name = u'设备申请信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.equipment
