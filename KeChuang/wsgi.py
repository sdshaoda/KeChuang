# coding:utf-8
import os
import sys

from django.core.wsgi import get_wsgi_application

# 部署时修改
# sys.path.append(r'C:/Users/sd/Desktop/sd/KeChuang/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KeChuang.settings")

application = get_wsgi_application()
