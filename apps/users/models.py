# coding:utf-8
from __future__ import unicode_literals

from datetime import datetime, date

from django.contrib.auth.models import AbstractUser
from django.db import models


# 部门信息
class Department(models.Model):
    name = models.CharField(unique=True, max_length=20, verbose_name=u'部门名称')
    # 用于区分 全公司 和 公司下的部门
    is_department = models.BooleanField(default=1, verbose_name=u'部门状态')
    remark = models.CharField(max_length=200, verbose_name=u'备注', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'部门信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 用户信息
class UserProfile(AbstractUser):
    department = models.ForeignKey(Department, verbose_name=u'所在部门', null=True, blank=True)
    department_name = models.CharField(max_length=20, verbose_name=u'部门名称', null=True, blank=True)

    name = models.CharField(max_length=10, verbose_name=u'姓名')
    username = models.CharField(unique=True, max_length=20, verbose_name=u'登录名')

    sex = models.CharField(max_length=2, choices=(
        ('男', u'男'),
        ('女', u'女'),
    ), verbose_name=u'性别')
    job = models.CharField(max_length=20, verbose_name=u'职务')
    induction_time = models.DateField(max_length=20, default=date.today, verbose_name=u'入职时间')
    permission = models.CharField(default=u'系统管理员', max_length=10, choices=(
        ('检测员', u'检测员'),
        ('部门负责', u'部门负责'),
        ('公司负责', u'公司负责'),
        ('系统管理员', u'系统管理员'),
    ), verbose_name=u'系统权限')
    number = models.CharField(max_length=20, verbose_name=u'人员编号')

    mobile = models.CharField(max_length=11, verbose_name=u'手机号码', null=True, blank=True)
    email = models.EmailField(max_length=20, verbose_name=u'邮箱地址', null=True, blank=True)
    office_phone = models.CharField(max_length=20, verbose_name=u'办公电话', null=True, blank=True)
    home_phone = models.CharField(max_length=20, verbose_name=u'家庭电话', null=True, blank=True)
    home_address = models.CharField(max_length=50, verbose_name=u'家庭住址', null=True, blank=True)
    xueli = models.CharField(max_length=50, verbose_name=u'学历', null=True, blank=True)
    zhicheng = models.CharField(max_length=50, verbose_name=u'职称', null=True, blank=True)
    zige = models.CharField(max_length=50, verbose_name=u'资格', null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', verbose_name=u'照片', max_length=100, null=True, blank=True)
    zigezs = models.FileField(upload_to='zige/%Y/%m', verbose_name=u'资格证书', max_length=100, null=True, blank=True)
    xuelizs = models.FileField(upload_to='xueli/%Y/%m', verbose_name=u'学历证书', max_length=100, null=True, blank=True)
    zhichengzs = models.FileField(upload_to='zhicheng/%Y/%m', verbose_name=u'职称证书', max_length=100, null=True,
                                  blank=True)

    def get_projects(self):
        return self.projectmember_set.filter(person_id=self.id, is_pro_person=1)

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'职工信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
