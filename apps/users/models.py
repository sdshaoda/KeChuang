# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    name = models.CharField(max_length=10, verbose_name=u'姓名')
    username = models.CharField(unique=True, max_length=20, verbose_name=u'登录名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号码')
    department = models.CharField(default='zhb', max_length=10, choices=(
        ("zhb", u"综合办"), ("zgb", u"总工办"), ("jc1s", u"检测一室"),
        ("jc2s", u"检测二室"), ("jc3s", u"检测三室"), ("jc4s", u"检测四室"),
        ("tlsys", u"土力学实验室"), ("ytlxsys", u"岩土力学实验室"),
        ("gjgs", u"钢结构室"), ("sbyfs", u"设备研发室")
    ), verbose_name=u'所在部门')
    job = models.CharField(max_length=20, verbose_name=u'职务')
    induction_time = models.DateField(max_length=20, default=datetime.now, verbose_name=u'入职时间')
    staff_num = models.CharField(max_length=20, verbose_name=u'职工编号')
    permission = models.CharField(default='0', max_length=2, choices=(
        ('0', u'检测员'), ('1', u'部门负责'), ('2', u'公司负责'), ('3', u'管理员'),
    ), verbose_name=u'系统权限')
    email = models.EmailField(max_length=20, verbose_name=u'邮箱地址', null=True, blank=True)
    office_phone = models.CharField(max_length=20, verbose_name=u'办公电话', null=True, blank=True)
    home_phone = models.CharField(max_length=20, verbose_name=u'家庭电话', null=True, blank=True)
    home_address = models.CharField(max_length=50, verbose_name=u'家庭住址', null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', verbose_name=u'照片', max_length=100, null=True, blank=True)
    zigezs = models.FileField(upload_to='zige/%Y/%m', verbose_name=u'资格证书', max_length=100, null=True, blank=True)
    xuelizs = models.FileField(upload_to='xueli/%Y/%m', verbose_name=u'学历证书', max_length=100, null=True, blank=True)
    zhichengzs = models.FileField(upload_to='zhicheng/%Y/%m', verbose_name=u'职称证书', max_length=100, null=True,
                                  blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'职工信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
