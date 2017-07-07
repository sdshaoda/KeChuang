# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


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
    pro_type = models.ForeignKey(ProjectType, verbose_name=u'工程类型', null=True, blank=True)
    pro_stage = models.ForeignKey(ProjectStage, verbose_name=u'项目阶段', null=True, blank=True)
    pro_type_name = models.CharField(max_length=20, verbose_name=u'工程类型名称', null=True, blank=True)
    pro_stage_name = models.CharField(max_length=20, verbose_name=u'项目阶段名称', null=True, blank=True)

    pro_name = models.CharField(max_length=50, verbose_name=u'工程名称')
    is_active = models.BooleanField(default=0, verbose_name=u'工程状态')

    department_id = models.IntegerField(verbose_name=u'所属部门id', null=True, blank=True)
    pro_person_id = models.IntegerField(verbose_name=u'工程负责人id', null=True, blank=True)
    wt_person_id = models.IntegerField(verbose_name=u'法人委托id', null=True, blank=True)
    ht_person_id = models.IntegerField(verbose_name=u'合同签署人id', null=True, blank=True)
    pro_person = models.CharField(max_length=20, verbose_name=u'工程负责人', null=True, blank=True)
    department = models.CharField(max_length=20, verbose_name=u'所属部门', null=True, blank=True)
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
    ht_scan = models.FileField(upload_to='hetong/%Y/%m', verbose_name=u'合同扫描件', max_length=100, null=True, blank=True)

    # report_num1 = models.CharField(max_length=30, verbose_name=u'报告编号1', null=True, blank=True)
    # report_num2 = models.CharField(max_length=30, verbose_name=u'报告编号2', null=True, blank=True)
    # report_num3 = models.CharField(max_length=30, verbose_name=u'报告编号3', null=True, blank=True)
    # report_num4 = models.CharField(max_length=30, verbose_name=u'报告编号4', null=True, blank=True)
    # report_num5 = models.CharField(max_length=30, verbose_name=u'报告编号5', null=True, blank=True)
    # report_author = models.CharField(max_length=10, verbose_name=u'报告编写人', null=True, blank=True)
    # report_checker = models.CharField(max_length=10, verbose_name=u'报告校核人', null=True, blank=True)
    # report_auditor = models.CharField(max_length=10, verbose_name=u'报告审核人', null=True, blank=True)
    # report_approver = models.CharField(max_length=10, verbose_name=u'报告批准人', null=True, blank=True)
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.pro_name


# 工程报告
class Report(models.Model):
    project = models.ForeignKey(Project, verbose_name=u'工程名称')
    title = models.CharField(max_length=30, verbose_name=u'标题')
    number = models.CharField(max_length=30, verbose_name=u'编号', null=True, blank=True)
    write_person = models.CharField(max_length=10, verbose_name=u'编写人', null=True, blank=True)
    check_person = models.CharField(max_length=10, verbose_name=u'校核人', null=True, blank=True)
    verify_person = models.CharField(max_length=10, verbose_name=u'审核人', null=True, blank=True)
    authorize_person = models.CharField(max_length=10, verbose_name=u'批准人', null=True, blank=True)
    file = models.FileField(upload_to='report/%Y/%m', verbose_name=u'报告文件', max_length=100, null=True, blank=True)

    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'工程报告'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
