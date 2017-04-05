# coding:utf-8
import xadmin

from .models import Announcement, Document


# 公告信息Admin
class AnnouncementAdmin(object):
    list_display = ['title', 'content', 'person', 'department', 'remark', 'add_time']
    search_fields = ['title', 'content', 'person', 'department', 'remark']
    list_filter = ['title', 'content', 'person', 'department', 'remark', 'add_time']


# 公文信息Admin
class DocumentAdmin(object):
    list_display = ['person', 'department', 'name', 'document', 'remark', 'add_time']
    search_fields = ['person', 'department', 'name', 'document', 'remark']
    list_filter = ['person', 'department', 'name', 'document', 'remark', 'add_time']


xadmin.site.register(Announcement, AnnouncementAdmin)
xadmin.site.register(Document, DocumentAdmin)
