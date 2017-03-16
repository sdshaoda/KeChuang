# coding:utf-8
from django.conf.urls import url

from .views import ListView, UseView, RevertView, InfoView, EditView, ApplyView, VerifyView

urlpatterns = [
    # 设备浏览
    url(r'^list/', ListView.as_view(), name='list'),
    # 设备领用
    url(r'^use/', UseView.as_view(), name='use'),
    # 设备归还
    url(r'^revert/', RevertView.as_view(), name='revert'),
    # 设备详细信息
    url(r'^info/', InfoView.as_view(), name='info'),
    # 设备编辑
    url(r'^edit/', EditView.as_view(), name='edit'),
    # 设备申请
    url(r'^apply/', ApplyView.as_view(), name='apply'),
    # 设备审核
    url(r'^verify/', VerifyView.as_view(), name='verify'),
]
