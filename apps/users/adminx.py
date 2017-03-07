# _*_ coding:utf-8 _*_
__author__ = 'shaoda'
__create_time__ = '2017/2/28 22:18'
import xadmin
from xadmin import views

from .models import UserProfile


# 修改 xadmin 的默认显示
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 修改 xadmin 的默认显示
class GlobalSettings(object):
    site_title = '武汉中科科创工程检测有限公司后台管理系统'
    site_footer = '武汉中科科创工程检测有限公司'
    menu_style = 'accordion'


class UserProfileAdmin(object):
    list_display = ['name', 'username', 'mobile', 'department', 'job', 'induction_time', 'staff_num', 'permission',
                    'email', 'office_phone', 'home_phone', 'home_address', 'image', 'zigezs', 'xuelizs', 'zhichengzs',
                    'add_time']
    search_fields = ['name', 'username', 'mobile', 'department', 'job', 'induction_time', 'staff_num', 'permission',
                     'email', 'office_phone', 'home_phone', 'home_address', 'image', 'zigezs', 'xuelizs', 'zhichengzs']
    list_filter = ['name', 'username', 'mobile', 'department', 'job', 'induction_time', 'staff_num', 'permission',
                   'email', 'office_phone', 'home_phone', 'home_address', 'image', 'zigezs', 'xuelizs', 'zhichengzs',
                   'add_time']


xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
