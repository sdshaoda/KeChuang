# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/28 21:13'
from django.conf.urls import url

from .views import ListView, EditView, EditStaffView, DeleteStaffView, AddressView, PermView, StaffView, ResetView, ChangeView, AddStaffView

urlpatterns = [
    # 人员浏览
    url(r'^list/', ListView.as_view(), name='list'),
    # 编辑档案 GET
    url(r'^edit/(?P<staff_id>\d+)$', EditView.as_view(), name='edit'),
    # 编辑档案 POST
    url(r'^staff/edit/$', EditStaffView.as_view(), name='edit_staff'),
    # 通讯录
    url(r'^address/', AddressView.as_view(), name='address'),
    # 人员权限管理
    url(r'^permission/', PermView.as_view(), name='permission'),
    # 员工信息管理
    url(r'^staff/', StaffView.as_view(), name='staff'),
    # 删除员工
    url(r'^staff/delete/', DeleteStaffView.as_view(), name='delete_staff'),
    # 添加新员工
    url(r'^add_staff/', AddStaffView.as_view(), name='add_staff'),
    # 重置密码
    url(r'^reset/', ResetView.as_view(), name='reset'),
    # 修改密码
    url(r'^change/', ChangeView.as_view(), name='change'),
]
