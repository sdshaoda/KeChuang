# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime, date

from django.db import models

from users.models import UserProfile


# 工程类型
class ProjectType(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'工程类型名称')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    # 类型下所有工程
    def get_projects(self):
        return self.project_set.filter(id=self.id)

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

    # 阶段下所有工程
    def get_projects(self):
        return self.project_set.filter(id=self.id)

    class Meta:
        verbose_name = u'项目阶段信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 工程信息
class Project(models.Model):
    pro_type = models.ForeignKey(ProjectType, verbose_name=u'工程类型', null=True, blank=True)
    pro_stage = models.ForeignKey(ProjectStage, verbose_name=u'项目阶段', null=True, blank=True)

    pro_name = models.CharField(max_length=50, verbose_name=u'工程名称')
    pro_person_id = models.IntegerField(verbose_name=u'工程负责人id')
    wt_person_id = models.IntegerField(verbose_name=u'法人委托id', null=True, blank=True)
    ht_person_id = models.IntegerField(verbose_name=u'合同签署人id', null=True, blank=True)

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
    ht_scan = models.FileField(upload_to='hetong/%Y/%m', verbose_name=u'合同扫描件', max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    # 工程负责人
    def get_pro_person(self):
        # return self.projectperson_set.get(id=self.id)
        return UserProfile.objects.get(id=self.pro_person_id)

    # 法人委托
    def get_wt_person(self):
        return UserProfile.objects.get(id=self.wt_person_id)

    # 合同签署人
    def get_ht_person(self):
        return UserProfile.objects.get(id=self.ht_person_id)

    # 工程成员
    def get_members(self):
        return self.projectmember_set.filter(id=self.id)

    # 工程设备
    def get_equipments(self):
        return self.projectequipment_set.filter(id=self.id)

    # 工程变更记录
    def get_change(self):
        return self.projectchange_set.filter(id=self.id).order_by('-add-time')

    class Meta:
        verbose_name = u'工程信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name


# 工程变更记录
class ProjectChange(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程名称')

    pro_type = models.CharField(max_length=20, verbose_name=u'工程类型')
    pro_stage = models.CharField(max_length=20, verbose_name=u'项目阶段', null=True, blank=True)

    pro_person_id = models.IntegerField(verbose_name=u'工程负责人id')
    wt_person_id = models.IntegerField(verbose_name=u'法人委托id', null=True, blank=True)
    ht_person_id = models.IntegerField(verbose_name=u'合同签署人id', null=True, blank=True)

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

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'修改时间')

    class Meta:
        verbose_name = u'工程变更记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.project
