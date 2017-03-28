# coding:utf-8
from django.conf.urls import url

from .views import ListView, UseView, UseEquView, RevertView, InfoView, EditView, ApplyView, VerifyView, AddView, \
    EditEquView, AgreeEquView, RefuseEquView

# namespace='equ'
urlpatterns = [
    # 设备浏览
    url(r'^list/', ListView.as_view(), name='list'),
    # 设备领用 GET
    url(r'^use/(?P<equ_id>\d+)$', UseView.as_view(), name='use'),
    # 设备领用 POST
    url(r'^equipment/use/', UseEquView.as_view(), name='equ_use'),
    # 设备归还
    url(r'^revert/', RevertView.as_view(), name='revert'),

    # 设备资料
    url(r'^info/', InfoView.as_view(), name='info'),
    # 添加设备
    url(r'^add/', AddView.as_view(), name='add'),
    # 编辑设备 GET
    url(r'^edit/(?P<equ_id>\d+)$', EditView.as_view(), name='edit'),
    # 编辑设备 Ajax
    url(r'^equipment/edit', EditEquView.as_view(), name='equ_edit'),

    # 设备申请
    url(r'^apply/', ApplyView.as_view(), name='apply'),
    # 设备审核
    url(r'^verify/', VerifyView.as_view(), name='verify'),
    # 同意领用
    url(r'^agree/', AgreeEquView.as_view(), name='agree'),
    # 拒绝领用
    url(r'^refuse/', RefuseEquView.as_view(), name='refuse'),
]
