# coding:utf-8
from django.shortcuts import render

from django.views.generic import View
from equipments.models import Equipment
from operation.models import EquipmentApply, ProjectEquipment


# 设备浏览
class ListView(View):
    def get(self, request):
        equs = Equipment.objects.all().order_by('-add_time')
        return render(request, 'equipment/list.html', {
            'equs': equs
        })


class UseView(View):
    def get(self, request):
        return render(request, 'equipment/use.html')


# 设备归还
class RevertView(View):
    def get(self, request):
        return render(request, 'equipment/revert.html')


# 设备资料
class InfoView(View):
    def get(self, request):
        return render(request, 'equipment/info.html')


# 添加设备
class AddView(View):
    def get(self, request):
        return render(request, 'equipment/info.html')


# 删除设备
class DeleteView(View):
    def get(self, request):
        return render(request, 'equipment/info.html')


# 编辑设备资料
class EditView(View):
    def get(self, request):
        return render(request, 'equipment/edit.html')


# 设备申请
class ApplyView(View):
    def get(self, request):
        return render(request, 'equipment/apply.html')


# 设备审核
class VerifyView(View):
    def get(self, request):
        return render(request, 'equipment/verify.html')
