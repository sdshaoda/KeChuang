# coding:utf-8
from django.conf.urls import url

from .views import ListView, UseView, UseEquView, RevertView, InfoView, EditView, ApplyView, VerifyView, AddView, \
    EditEquView, AgreeEquView, RefuseEquView, RevertEquView, ChangeRevertDateView, EquUseRecordView

# namespace='equ'
urlpatterns = [
    # 设备浏览 GET
    url(r'^list/$', ListView.as_view(), name='list'),
    # 设备领用 GET
    url(r'^use/(?P<equ_id>\d+)$', UseView.as_view(), name='use'),
    # 设备领用 POST
    url(r'^equipment/use/$', UseEquView.as_view(), name='equ_use'),
    # 设备归还 GET
    url(r'^revert/$', RevertView.as_view(), name='revert'),
    # 设备归还 Ajax
    url(r'^equipment/revert/$', RevertEquView.as_view(), name='equ_revert'),

    # 设备资料 GET
    url(r'^info/$', InfoView.as_view(), name='info'),
    # 添加设备 GET POST
    url(r'^add/$', AddView.as_view(), name='add'),
    # 编辑设备 GET
    url(r'^edit/(?P<equ_id>\d+)$', EditView.as_view(), name='edit'),
    # 编辑设备 Ajax
    url(r'^equipment/edit/$', EditEquView.as_view(), name='equ_edit'),
    # 使用记录 GET
    url(r'^equipment/use_record/$', EquUseRecordView.as_view(), name='use_record'),

    # 设备申请 GET
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    # 设备审核 GET
    url(r'^verify/$', VerifyView.as_view(), name='verify'),
    # 同意领用 Ajax
    url(r'^agree/$', AgreeEquView.as_view(), name='agree'),
    # 拒绝领用 Ajax
    url(r'^refuse/$', RefuseEquView.as_view(), name='refuse'),
    # 修改归还时间
    url(r'^change/revert_date$', ChangeRevertDateView.as_view(), name='change_revert_date'),
]
