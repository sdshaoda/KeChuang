# _*_ coding:utf-8 _*_
from django.conf.urls import url

from .views import ListView, EditView, AddProView, VerifyView, DetailView, ApplyView, DeleteView, LocalView

urlpatterns = [
    # 工程浏览
    url(r'^list/', ListView.as_view(), name='list'),
    # 添加工程
    url(r'^add/$', AddProView.as_view(), name='add'),
    # 编辑工程
    url(r'^edit/(?P<pro_id>\d+)$', EditView.as_view(), name='edit'),
    # 工程详情
    url(r'^detail/(?P<pro_id>\d+)$', DetailView.as_view(), name='detail'),
    # 删除工程
    url(r'^delete/', DeleteView.as_view(), name='address'),
    # 工程申请
    url(r'^apply/', ApplyView.as_view(), name='apply'),
    # 工程审核
    url(r'^verify/', VerifyView.as_view(), name='verify'),
    # 现场管理
    url(r'^local/', LocalView.as_view(), name='local'),
]
