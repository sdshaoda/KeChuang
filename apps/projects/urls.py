# coding:utf-8
from django.conf.urls import url

from .views import ListView, EditView, AddProView, VerifyView, DetailView, ApplyView, DeleteView, AttendanceView, EditProView, ChangeView, ApplyDetailView, AgreeProView, RefuseProView, AddAttendanceView

# namespace='pro'
urlpatterns = [
    # 添加工程 GET POST
    url(r'^add/$', AddProView.as_view(), name='add'),
    # 工程浏览 GET
    url(r'^list/$', ListView.as_view(), name='list'),
    # 编辑工程 GET
    url(r'^edit/(?P<pro_id>\d+)$', EditView.as_view(), name='edit'),
    # 编辑工程 POST
    url(r'^project/edit/$', EditProView.as_view(), name='pro_edit'),
    # 工程详情 GET
    url(r'^detail/(?P<pro_id>\d+)$', DetailView.as_view(), name='detail'),
    # 删除工程 Ajax
    url(r'^delete/$', DeleteView.as_view(), name='delete'),

    # 工程申请 GET
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    # 申请详情 GET
    url(r'^apply/detail/(?P<pro_apply_id>\d+)$', ApplyDetailView.as_view(), name='pro_apply'),
    # 工程审核 GET
    url(r'^verify/$', VerifyView.as_view(), name='verify'),
    # 同意申请 Ajax
    url(r'^agree/$', AgreeProView.as_view(), name='agree'),
    # 拒绝申请 Ajax
    url(r'^refuse/$', RefuseProView.as_view(), name='refuse'),

    # 考勤记录 GET
    url(r'^attendance/$', AttendanceView.as_view(), name='attendance'),
    # 添加考勤 GET POST
    url(r'^add/attendance/$', AddAttendanceView.as_view(), name='add_attendance'),
    # 变更信息 GET
    url(r'^change/$', ChangeView.as_view(), name='change'),
]
