# coding:utf-8
import xadmin

from .models import ProjectMember, ProjectEquipment, ProjectApply, EquipmentApply, ProjectAttendance


# 工程负责人Admin
# class ProjectPersonAdmin(object):
#     list_display = ['project', 'person', 'remark', 'add_time']
#     search_fields = ['project', 'person', 'remark']
#     list_filter = ['project', 'person', 'remark', 'add_time']


# 工程项目成员Admin
class ProjectMemberAdmin(object):
    list_display = ['project', 'person', 'department', 'remark', 'add_time']
    search_fields = ['project', 'person', 'department', 'remark']
    list_filter = ['project', 'person', 'department', 'remark', 'add_time']


# 工程考勤Admin
class ProjectAttendanceAdmin(object):
    list_display = ['project', 'person', 'department', 'location', 'time', 'remark', 'add_time']
    search_fields = ['project', 'person', 'department', 'location', 'remark']
    list_filter = ['project', 'person', 'department', 'location', 'time', 'remark', 'add_time']


# 工程设备Admin
class ProjectEquipmentAdmin(object):
    list_display = ['project', 'equipment', 'remark', 'add_time']
    search_fields = ['project', 'equipment', 'remark']
    list_filter = ['project', 'equipment', 'remark', 'add_time']


# 工程申请Admin
class ProjectApplyAdmin(object):
    list_display = ['project', 'person', 'type', 'status', 'pro_type', 'pro_stage', 'department',
                    'pro_person', 'wt_person', 'ht_person', 'ht_name', 'ht_num', 'ht_money', 'js_money', 'wt_dw',
                    'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date', 'ht_scan', 'remark', 'add_time']
    search_fields = ['project', 'person', 'type', 'status', 'pro_type', 'pro_stage', 'department',
                    'pro_person', 'wt_person', 'ht_person', 'ht_name', 'ht_num', 'ht_money', 'js_money', 'wt_dw',
                    'mobile', 'pro_address', 'ht_scan', 'remark']
    list_filter = ['project', 'person', 'type', 'status', 'pro_type', 'pro_stage', 'department',
                    'pro_person', 'wt_person', 'ht_person', 'ht_name', 'ht_num', 'ht_money', 'js_money', 'wt_dw',
                    'mobile', 'pro_address', 'sign_date', 'start_date', 'finish_date', 'ht_scan', 'remark', 'add_time']


# 设备负责人Admin
# class EquipmentPersonAdmin(object):
#     list_display = ['equipment', 'person', 'remark', 'add_time']
#     search_fields = ['equipment', 'person', 'remark']
#     list_filter = ['equipment', 'person', 'remark', 'add_time']


# 设备保管人Admin
# class EquipmentStaffAdmin(object):
#     list_display = ['equipment', 'person', 'remark', 'add_time']
#     search_fields = ['equipment', 'person', 'remark']
#     list_filter = ['equipment', 'person', 'remark', 'add_time']


# 设备申请Admin
class EquipmentApplyAdmin(object):
    list_display = ['equipment', 'person', 'equipment_person', 'type', 'status', 'use_date', 'revert_date', 'remark',
                    'add_time']
    search_fields = ['equipment', 'person', 'equipment_person', 'type', 'status', 'use_date', 'revert_date', 'remark']
    list_filter = ['equipment', 'person', 'equipment_person', 'type', 'status', 'use_date', 'revert_date', 'remark',
                   'add_time']


# xadmin.site.register(ProjectPerson, ProjectPersonAdmin)
xadmin.site.register(ProjectMember, ProjectMemberAdmin)
xadmin.site.register(ProjectAttendance, ProjectAttendanceAdmin)
xadmin.site.register(ProjectEquipment, ProjectEquipmentAdmin)
xadmin.site.register(ProjectApply, ProjectApplyAdmin)

# xadmin.site.register(EquipmentPerson, EquipmentPersonAdmin)
# xadmin.site.register(EquipmentStaff, EquipmentStaffAdmin)
xadmin.site.register(EquipmentApply, EquipmentApplyAdmin)
