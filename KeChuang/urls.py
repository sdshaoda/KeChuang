# coding:utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView

from KeChuang.settings import MEDIA_ROOT

import xadmin
from users.views import LoginView, LogoutView

urlpatterns = [
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
    # 登录 GET POST
    url(r'^$', LoginView.as_view(), name='login'),
    # 退出 GET
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 后台
    url(r'^admin/', xadmin.site.urls),
    # 文件上传
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 静态文件
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # 用户管理
    url(r'^user/', include('users.urls', namespace='user')),
    # 工程管理
    url(r'^project/', include('projects.urls', namespace='pro')),
    # 设备管理
    url(r'^equipment/', include('equipments.urls', namespace='equ')),
    # 公告管理
    url(r'^announcement/', include('announcements.urls', namespace='ann')),
]

# 全局 404 页面
handler404 = 'users.views.page_not_found'
# 全局 500 页面
handler500 = 'users.views.page_error'
