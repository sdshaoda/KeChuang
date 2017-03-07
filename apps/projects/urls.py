# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/28 21:13'
from django.conf.urls import url

from .views import ListView, AddProView, VerifyView, DetailView, EditView, ApplyView

urlpatterns = [
    # 浏览工程
    url(r'^list/', ListView.as_view(), name='list'),
    # 添加工程
    url(r'^add/', AddProView.as_view(), name='add'),
    # 编辑工程
    url(r'^edit/', EditView.as_view(), name='edit'),
    # 删除工程
    url(r'^delete/', EditView.as_view(), name='delete'),
    # 工程申请
    url(r'^apply/', ApplyView.as_view(), name='apply'),
    # 工程审核
    url(r'^verify/', VerifyView.as_view(), name='verify'),
    # 工程详细信息
    url(r'^detail/(?P<pro_id>\d+)$', DetailView.as_view(), name='detail'),
]
