# coding:utf-8
import xadmin

from .models import Project, ProjectStage, ProjectType


# 工程类型Admin
class ProjectTypeAdmin(object):
    list_display = ['name', 'remark', 'add_time']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark', 'add_time']


# 项目阶段Admin
class ProjectStageAdmin(object):
    list_display = ['name', 'remark', 'add_time']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark', 'add_time']


# 工程信息Admin
class ProjectAdmin(object):
    list_display = ['pro_type', 'pro_stage', 'pro_name', 'department', 'pro_person', 'wt_person', 'ht_person',
                    'ht_name',
                    'ht_num',
                    'ht_money', 'js_money', 'wt_dw', 'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date',
                    'remark', 'add_time']
    search_fields = ['pro_type', 'pro_stage', 'pro_name', 'department', 'pro_person', 'wt_person', 'ht_person',
                     'ht_name',
                     'ht_num',
                     'ht_money', 'js_money', 'wt_dw', 'mobile', 'pro_address',
                     'remark']
    list_filter = ['pro_type', 'pro_stage', 'pro_name', 'department', 'pro_person', 'wt_person', 'ht_person', 'ht_name',
                   'ht_num',
                   'ht_money', 'js_money', 'wt_dw', 'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date',
                   'remark', 'add_time']


# 工程变更记录Admin
# class ProjectChangeAdmin(object):
#     list_display = ['project', 'pro_type', 'pro_stage', 'pro_person', 'wt_person', 'ht_person', 'ht_name', 'ht_num',
#                     'ht_money', 'js_money', 'wt_dw', 'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date',
#                     'remark', 'add_time']
#     search_fields = ['project', 'pro_type', 'pro_stage', 'pro_person', 'wt_person', 'ht_person', 'ht_name', 'ht_num',
#                      'ht_money', 'js_money', 'wt_dw', 'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date',
#                      'remark']
#     list_filter = ['project', 'pro_type', 'pro_stage', 'pro_person', 'wt_person', 'ht_person', 'ht_name', 'ht_num',
#                    'ht_money', 'js_money', 'wt_dw', 'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date',
#                    'remark', 'add_time']


xadmin.site.register(ProjectType, ProjectTypeAdmin)
xadmin.site.register(ProjectStage, ProjectStageAdmin)
xadmin.site.register(Project, ProjectAdmin)
# xadmin.site.register(ProjectChange, ProjectChangeAdmin)
