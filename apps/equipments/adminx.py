# coding:utf-8
import xadmin

from .models import Equipment, EquipmentType


# 设备类型Admin
class EquipmentTypeAdmin(object):
    list_display = ['name', 'remark', 'add_time']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark', 'add_time']


# 设备信息Admin
class EquipmentAdmin(object):
    list_display = ['equ_type', 'equ_name', 'equ_person', 'file_num', 'equ_num', 'equ_status', 'effect_date',
                    'equ_money',
                    'buy_date', 'use_status', 'equ_staff', 'use_date', 'revert_date', 'remark', 'add_time']
    search_fields = ['equ_type', 'equ_name', 'equ_person', 'file_num', 'equ_num', 'equ_status', 'effect_date',
                     'equ_money',
                     'buy_date', 'use_status', 'equ_staff', 'use_date', 'revert_date', 'remark', 'add_time']
    list_filter = ['equ_type', 'equ_name', 'equ_person', 'file_num', 'equ_num', 'equ_status', 'effect_date',
                   'equ_money',
                   'buy_date', 'use_status', 'equ_staff', 'use_date', 'revert_date', 'remark', 'add_time']


# 设备变更记录Admin
# class EquipmentChangeAdmin(object):
# list_display = ['equipment', 'equi_type', 'equi_person', 'equi_num', 'equi_status', 'effect_date', 'equi_money',
#                 'buy_date', 'person', 'department', 'use_date', 'revert_date', 'remark', 'add_time']
# search_fields = ['equipment', 'equi_type', 'equi_person', 'equi_num', 'equi_status', 'effect_date', 'equi_money',
#                  'buy_date', 'person', 'department', 'use_date', 'revert_date', 'remark']
# list_filter = ['equipment', 'equi_type', 'equi_person', 'equi_num', 'equi_status', 'effect_date', 'equi_money',
#                'buy_date', 'person', 'department', 'use_date', 'revert_date', 'remark', 'add_time']


xadmin.site.register(EquipmentType, EquipmentTypeAdmin)
xadmin.site.register(Equipment, EquipmentAdmin)
# xadmin.site.register(EquipmentChange, EquipmentChangeAdmin)
