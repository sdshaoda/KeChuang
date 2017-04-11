# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime, date

from django.db import models

from equipments.models import Equipment
from projects.models import Project
from users.models import UserProfile, Department


# 工程负责人
# class ProjectPerson(models.Model):
#     project = models.ForeignKey(Project, verbose_name=u'工程名称')
#     person = models.ForeignKey(UserProfile, verbose_name=u'负责人')
#
#     remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)
#
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#
#     class Meta:
#         verbose_name = u'工程负责人信息'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.project


# 工程项目成员
class ProjectMember(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程')
    person = models.ForeignKey(UserProfile, verbose_name=u'项目成员')
    project_name = models.CharField(max_length=50, verbose_name=u'工程名称', null=True, blank=True)
    person_name = models.CharField(max_length=20, verbose_name=u'项目成员名称', null=True, blank=True)

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'项目成员信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 工程考勤
class ProjectAttendance(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程')
    person = models.ForeignKey(UserProfile, verbose_name=u'考勤人员')
    project_name = models.CharField(max_length=50, verbose_name=u'工程名称', null=True, blank=True)
    person_name = models.CharField(max_length=20, verbose_name=u'考勤人员名称', null=True, blank=True)

    location = models.CharField(max_length=50, verbose_name=u'地点')
    time = models.DateTimeField(verbose_name=u'时间')

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'登记时间')

    class Meta:
        verbose_name = u'工程考勤信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 工程设备
class ProjectEquipment(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程')
    equipment = models.ForeignKey(Equipment, verbose_name=u'检测设备')
    project_name = models.CharField(max_length=50, verbose_name=u'工程名称', null=True, blank=True)
    equipment_name = models.CharField(max_length=20, verbose_name=u'检测设备名称', null=True, blank=True)

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程设备信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 工程申请
class ProjectApply(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程')
    person = models.ForeignKey(UserProfile, verbose_name=u'申请人')
    project_name = models.CharField(max_length=50, verbose_name=u'工程名称', null=True, blank=True)
    person_name = models.CharField(max_length=20, verbose_name=u'申请人名称', null=True, blank=True)

    # 申请相关
    type = models.CharField(max_length=4, choices=(
        ('添加工程', u'添加工程'), ('修改信息', u'修改信息'), ('删除工程', u'删除工程')
    ), verbose_name=u'申请类型')
    status = models.CharField(default='0', max_length=10, choices=(
        ('部门主任审核中', u'部门主任审核中'), ('公司领导审核中', u'公司领导审核中'), ('审核通过', u'审核通过'), ('审核未通过', u'审核未通过')
    ), verbose_name=u'审核状态')

    # 信息相关
    pro_type_id = models.IntegerField(verbose_name=u'工程类型id', null=True, blank=True)
    pro_stage_id = models.IntegerField(verbose_name=u'项目阶段id', null=True, blank=True)
    department_id = models.IntegerField(verbose_name=u'所属部门id', null=True, blank=True)
    pro_person_id = models.IntegerField(verbose_name=u'工程负责人id', null=True, blank=True)
    wt_person_id = models.IntegerField(verbose_name=u'法人委托id', null=True, blank=True)
    ht_person_id = models.IntegerField(verbose_name=u'合同签署人id', null=True, blank=True)
    pro_type = models.CharField(max_length=20, verbose_name=u'工程类型', null=True, blank=True)
    pro_stage = models.CharField(max_length=20, verbose_name=u'项目阶段', null=True, blank=True)
    department = models.CharField(max_length=20, verbose_name=u'所属部门', null=True, blank=True)
    pro_person = models.CharField(max_length=20, verbose_name=u'工程负责人', null=True, blank=True)
    wt_person = models.CharField(max_length=20, verbose_name=u'法人委托', null=True, blank=True)
    ht_person = models.CharField(max_length=20, verbose_name=u'合同签署人', null=True, blank=True)

    ht_name = models.CharField(max_length=50, verbose_name=u'合同名称', null=True, blank=True)
    ht_num = models.CharField(max_length=50, verbose_name=u'合同编号', null=True, blank=True)
    ht_money = models.CharField(max_length=20, verbose_name=u'合同金额', null=True, blank=True)
    js_money = models.CharField(max_length=20, verbose_name=u'结算金额', null=True, blank=True)
    wt_dw = models.CharField(max_length=50, verbose_name=u'委托单位', null=True, blank=True)
    mobile = models.CharField(max_length=20, verbose_name=u'联系电话', null=True, blank=True)
    pro_address = models.CharField(max_length=50, verbose_name=u'项目地址', null=True, blank=True)
    sign_date = models.DateField(max_length=20, verbose_name=u'签订日期', null=True, blank=True)
    start_date = models.DateField(max_length=20, verbose_name=u'开工日期', null=True, blank=True)
    finish_date = models.DateField(max_length=20, verbose_name=u'完工日期', null=True, blank=True)
    ht_scan = models.FileField(max_length=100, upload_to='hetong/%Y/%m', verbose_name=u'合同扫描件', null=True, blank=True)
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'申请时间')

    class Meta:
        verbose_name = u'工程申请信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project


# 设备负责人
# class EquipmentPerson(models.Model):
#     equipment = models.ForeignKey(Equipment, verbose_name=u'设备名称')
#     person = models.ForeignKey(UserProfile, verbose_name=u'负责人', null=True, blank=True)
#
#     remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)
#
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#
#     class Meta:
#         verbose_name = u'设备负责人信息'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.equipment


# 设备保管人
# class EquipmentStaff(models.Model):
#     equipment = models.ForeignKey(Equipment, verbose_name=u'设备名称')
#     person = models.ForeignKey(UserProfile, verbose_name=u'保管人', null=True, blank=True)
#
#     remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)
#
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
#
#     class Meta:
#         verbose_name = u'设备保管人信息'
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.equipment


# 设备申请
class EquipmentApply(models.Model):
    # 设备申请信息
    equipment = models.ForeignKey(Equipment, verbose_name=u'设备')
    person = models.ForeignKey(UserProfile, verbose_name=u'申请人')
    equipment_name = models.CharField(max_length=50, verbose_name=u'设备名称', null=True, blank=True)
    person_name = models.CharField(max_length=20, verbose_name=u'申请人名称', null=True, blank=True)

    equipment_person_id = models.IntegerField(verbose_name=u'设备负责人id', null=True, blank=True)
    equipment_person = models.CharField(max_length=20, verbose_name=u'设备负责人', null=True, blank=True)

    type = models.CharField(default='0', max_length=2, choices=(
        ('领用', u'领用'), ('归还', u'归还')
    ), verbose_name=u'申请类型')
    status = models.CharField(default='0', max_length=2, choices=(
        ('审核中', u'审核中'), ('审核通过', u'审核通过'), ('审核未通过', u'审核未通过')
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
