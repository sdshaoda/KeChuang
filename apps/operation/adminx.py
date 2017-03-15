# coding:utf-8
import xadmin

from .models import ProjectEquipment, ProjectApply, EquipmentApply


# 工程设备Admin
class ProjectEquipmentAdmin(object):
    list_display = ['pro_name', 'equipment', 'add_time']
    search_fields = ['pro_name', 'equipment', 'add_time']
    list_filter = ['pro_name', 'equipment', 'add_time']


# 工程申请Admin
class ProjectApplyAdmin(object):
    list_display = ['pro_name', 'person', 'type', 'remark', 'status', 'add_time']
    search_fields = ['pro_name', 'person', 'type', 'remark', 'status']
    list_filter = ['pro_name', 'person', 'type', 'remark', 'status', 'add_time']


# 设备申请Admin
class EquipmentApplyAdmin(object):
    list_display = ['equi_name', 'person', 'type', 'remark', 'status', 'add_time']
    search_fields = ['equi_name', 'person', 'type', 'remark', 'status']
    list_filter = ['equi_name', 'person', 'type', 'remark', 'status', 'add_time']


xadmin.site.register(ProjectEquipment, ProjectEquipmentAdmin)
xadmin.site.register(ProjectApply, ProjectApplyAdmin)
xadmin.site.register(EquipmentApply, EquipmentApplyAdmin)
