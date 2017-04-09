# coding:utf-8
import xadmin
from xadmin import views

from .models import Department, UserProfile


# 修改 xadmin 的默认显示
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 修改 xadmin 的默认显示
class GlobalSettings(object):
    site_title = '武汉中科科创工程检测有限公司-后台管理系统'
    site_footer = '武汉中科科创工程检测有限公司'
    # menu_style = 'accordion'


# 部门信息Admin
class DepartmentAdmin(object):
    list_display = ['name', 'remark', 'add_time']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark', 'add_time']


# 用户信息Admin
class UserProfileAdmin(object):
    list_display = ['department', 'name', 'sex', 'username', 'job', 'induction_time', 'permission', 'number', 'mobile',
                    'email', 'office_phone', 'home_phone', 'home_address', 'xueli', 'zhicheng', 'zige', 'image',
                    'zigezs', 'xuelizs', 'zhichengzs',
                    'add_time']
    search_fields = ['department', 'name', 'sex', 'username', 'job', 'induction_time', 'permission', 'number', 'mobile',
                     'email', 'office_phone', 'home_phone', 'home_address', 'xueli', 'zhicheng', 'zige', 'image',
                     'zigezs', 'xuelizs', 'zhichengzs']
    list_filter = ['department', 'name', 'sex', 'username', 'job', 'induction_time', 'permission', 'number', 'mobile',
                   'email', 'office_phone', 'home_phone', 'home_address', 'xueli', 'zhicheng', 'zige', 'image',
                   'zigezs', 'xuelizs', 'zhichengzs',
                   'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
