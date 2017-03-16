# coding:utf-8
from django.conf.urls import url

from .views import ListView, PublishView, DetailView, DocListView, DeleteAnnView, DocUploadView

urlpatterns = [
    # 浏览公告
    url(r'^list/', ListView.as_view(), name='list'),
    # 发布公告
    url(r'^publish/', PublishView.as_view(), name='publish'),
    # 删除公告
    url(r'^ann/delete/', DeleteAnnView.as_view(), name='delete_ann'),
    # 公告详细信息
    url(r'^detail/(?P<ann_id>\d+)$', DetailView.as_view(), name='detail'),
    # 公文管理
    url(r'^document/list', DocListView.as_view(), name='doc_list'),
    # 上传公文
    url(r'^document/upload', DocUploadView.as_view(), name='doc_upload'),
]
