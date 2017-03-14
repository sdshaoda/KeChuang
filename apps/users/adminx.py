# _*_ coding:utf-8 _*_
import xadmin
from xadmin import views

from .models import Department, UserProfile


# 修改 xadmin 的默认显示
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 修改 xadmin 的默认显示
class GlobalSettings(object):
    site_title = '武汉中科科创工程检测有限公司后台管理系统'
    site_footer = '武汉中科科创工程检测有限公司'
    menu_style = 'accordion'


class DepartmentAdmin(object):
    list_display = ['name', 'remark', 'add_time']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark', 'add_time']


class UserProfileAdmin(object):
    list_display = ['name', 'username', 'mobile', 'department', 'job', 'induction_time', 'permission',
                    'email', 'office_phone', 'home_phone', 'home_address', 'image', 'zigezs', 'xuelizs', 'zhichengzs',
                    'add_time']
    search_fields = ['name', 'username', 'mobile', 'department', 'job', 'induction_time', 'permission',
                     'email', 'office_phone', 'home_phone', 'home_address', 'image', 'zigezs', 'xuelizs', 'zhichengzs']
    list_filter = ['name', 'username', 'mobile', 'department', 'job', 'induction_time', 'permission',
                   'email', 'office_phone', 'home_phone', 'home_address', 'image', 'zigezs', 'xuelizs', 'zhichengzs',
                   'add_time']


xadmin.site.register(Department, DepartmentAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
