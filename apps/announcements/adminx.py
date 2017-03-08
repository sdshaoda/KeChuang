# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/28 22:18'

import xadmin

from .models import Announcement, Document


class AnnouncementAdmin(object):
    list_display = ['title', 'content', 'person', 'department', 'add_time']
    search_fields = ['title', 'content', 'person', 'department']
    list_filter = ['title', 'content', 'person', 'department', 'add_time']


class DocumentAdmin(object):
    list_display = ['name', 'document', 'add_time']
    search_fields = ['name', 'document']
    list_filter = ['name', 'document', 'add_time']


xadmin.site.register(Announcement, AnnouncementAdmin)
xadmin.site.register(Document, DocumentAdmin)