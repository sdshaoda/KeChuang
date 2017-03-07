# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_date__ = '2017/2/28 22:18'

import xadmin

from .models import Project


class ProjectAdmin(object):
    list_display = ['pro_person', 'pro_name', 'ht_name', 'ht_num', 'ht_money', 'wt_dw', 'wt_person', 'mobile',
                    'pro_address', 'represent_person', 'sign_date', 'start_date', 'finish_date', 'pro_type',
                    'equipment', 'ht_scan', 'add_time']
    search_fields = ['pro_person', 'pro_name', 'ht_name', 'ht_num', 'ht_money', 'wt_dw', 'wt_person', 'mobile',
                     'pro_address', 'represent_person', 'sign_date', 'start_date', 'finish_date', 'pro_type',
                     'equipment', 'ht_scan']
    list_filter = ['pro_person', 'pro_name', 'ht_name', 'ht_num', 'ht_money', 'wt_dw', 'wt_person', 'mobile',
                   'pro_address', 'represent_person', 'sign_date', 'start_date', 'finish_date', 'pro_type',
                   'equipment', 'ht_scan', 'add_time']


xadmin.site.register(Project, ProjectAdmin)
