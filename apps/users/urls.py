# coding:utf-8
from django.conf.urls import url

from .views import ListView, EditView, EditStaffView, DeleteStaffView, AddressView, PermView, StaffView, ResetView, \
    ChangeView, AddStaffView

# namespace='user'
urlpatterns = [
    # 人员浏览 GET
    url(r'^list/$', ListView.as_view(), name='list'),
    # 编辑档案 GET
    url(r'^edit/(?P<staff_id>\d+)$', EditView.as_view(), name='edit'),
    # 编辑档案 Ajax
    url(r'^staff/edit/$', EditStaffView.as_view(), name='edit_staff'),
    # 通讯录 GET
    url(r'^address/$', AddressView.as_view(), name='address'),

    # 人员权限管理 GET Ajax
    url(r'^permission/$', PermView.as_view(), name='permission'),
    # 员工信息管理 GET
    url(r'^staff/$', StaffView.as_view(), name='staff'),
    # 添加新员工 GET POST
    url(r'^add_staff/$', AddStaffView.as_view(), name='add_staff'),
    # 删除员工 Ajax
    url(r'^staff/delete/$', DeleteStaffView.as_view(), name='delete_staff'),

    # 重置密码 GET Ajax
    url(r'^reset/$', ResetView.as_view(), name='reset'),
    # 修改密码 GET Ajax
    url(r'^change/$', ChangeView.as_view(), name='change'),
]
