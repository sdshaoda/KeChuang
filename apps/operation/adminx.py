# coding:utf-8
import xadmin

from .models import ProjectMember, ProjectEquipment, ProjectApply, EquipmentApply, ProjectAttendance, ProjectPerson, EquipmentPerson, EquipmentStaff


# 工程负责人Admin
class ProjectPersonAdmin(object):
    list_display = ['project', 'person', 'remark', 'add_time']
    search_fields = ['project', 'person', 'remark']
    list_filter = ['project', 'person', 'remark', 'add_time']


# 工程项目成员Admin
class ProjectMemberAdmin(object):
    list_display = ['project', 'member', 'remark', 'add_time']
    search_fields = ['project', 'member', 'remark']
    list_filter = ['project', 'member', 'remark', 'add_time']


# 工程考勤Admin
class ProjectAttendanceAdmin(object):
    list_display = ['project', 'person', 'location', 'time', 'remark', 'add_time']
    search_fields = ['project', 'person', 'location', 'time', 'remark']
    list_filter = ['project', 'person', 'location', 'time', 'remark', 'add_time']


# 工程设备Admin
class ProjectEquipmentAdmin(object):
    list_display = ['project', 'equipment', 'remark', 'add_time']
    search_fields = ['project', 'equipment', 'remark']
    list_filter = ['project', 'equipment', 'remark', 'add_time']


# 工程申请Admin
class ProjectApplyAdmin(object):
    list_display = ['project', 'person', 'type', 'remark', 'status', 'add_time']
    search_fields = ['project', 'person', 'type', 'remark', 'status']
    list_filter = ['project', 'person', 'type', 'remark', 'status', 'add_time']


# 设备负责人Admin
class EquipmentPersonAdmin(object):
    list_display = ['equipment', 'person', 'remark', 'add_time']
    search_fields = ['equipment', 'person', 'remark']
    list_filter = ['equipment', 'person', 'remark', 'add_time']


# 设备保管人Admin
class EquipmentStaffAdmin(object):
    list_display = ['equipment', 'person', 'remark', 'add_time']
    search_fields = ['equipment', 'person', 'remark']
    list_filter = ['equipment', 'person', 'remark', 'add_time']


# 设备申请Admin
class EquipmentApplyAdmin(object):
    list_display = ['equipment', 'person', 'type', 'status', 'use_date', 'revert_date', 'remark', 'add_time']
    search_fields = ['equipment', 'person', 'type', 'status', 'use_date', 'revert_date', 'remark']
    list_filter = ['equipment', 'person', 'type', 'status', 'use_date', 'revert_date', 'remark', 'add_time']


xadmin.site.register(ProjectPerson, ProjectPersonAdmin)
xadmin.site.register(ProjectMember, ProjectMemberAdmin)
xadmin.site.register(ProjectAttendance, ProjectAttendanceAdmin)
xadmin.site.register(ProjectEquipment, ProjectEquipmentAdmin)
xadmin.site.register(ProjectApply, ProjectApplyAdmin)

xadmin.site.register(EquipmentPerson, EquipmentPersonAdmin)
xadmin.site.register(EquipmentStaff, EquipmentStaffAdmin)
xadmin.site.register(EquipmentApply, EquipmentApplyAdmin)
