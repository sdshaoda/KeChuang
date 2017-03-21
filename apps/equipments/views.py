# coding:utf-8
from django.shortcuts import render

from django.views.generic import View
from users.models import UserProfile
from equipments.models import Equipment, EquipmentType
from operation.models import EquipmentApply, ProjectEquipment


# 设备浏览
class ListView(View):
    def get(self, request):
        equs = Equipment.objects.all().order_by('-add_time')
        return render(request, 'equipment/list.html', {
            'equs': equs
        })


# 设备领用
class UseView(View):
    def get(self, request, equ_id):
        equ = Equipment.objects.get(id=equ_id)
        return render(request, 'equipment/use.html', {
            'equ': equ
        })


# 设备领用 POST
class UseEquView(View):
    def post(self, request):
        return render(request, 'equipment/apply.html', {})


# 设备归还
class RevertView(View):
    def get(self, request):
        return render(request, 'equipment/revert.html')


# 设备资料
class InfoView(View):
    def get(self, request):
        equs = Equipment.objects.all().order_by('-add_time')
        return render(request, 'equipment/info.html', {
            'equs': equs
        })


# 添加设备
class AddView(View):
    def get(self, request):
        equ_types = EquipmentType.objects.all().order_by('-add_time')

        # 筛除超级用户
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

        return render(request, 'equipment/edit.html', {
            'equ_types': equ_types,
            'staffs': staffs,
            'type': 'add'
        })

    def post(self, request):
        equi_name = request.POST.get('equi_name', '')
        equi_type_id = request.POST.get('equi_type', '')
        equi_person_id = request.POST.get('equi_person', '')
        equi_num = request.POST.get('equi_num', '')
        equi_status = request.POST.get('equi_status', '')
        effect_date = request.POST.get('effect_date', '')
        equi_money = request.POST.get('equi_money', '')
        buy_date = request.POST.get('buy_date', '')
        remark = request.POST.get('remark', '')

        equipment = Equipment()
        equipment.equi_name = equi_name
        equipment.equi_type = EquipmentType.objects.get(id=equi_type_id)
        equipment.equi_person = UserProfile.objects.get(id=equi_person_id)
        equipment.equi_num = equi_num
        equipment.equi_status = equi_status
        equipment.effect_date = effect_date
        equipment.equi_money = equi_money
        equipment.buy_date = buy_date
        equipment.remark = remark
        equipment.save()

        equs = Equipment.objects.all().order_by('-add_time')
        return render(request, 'equipment/info.html', {
            'equs': equs
        })


# 删除设备
class DeleteView(View):
    def get(self, request):
        return render(request, 'equipment/info.html')


# 编辑设备资料
class EditView(View):
    def get(self, request, equ_id):
        equ = Equipment.objects.get(id=equ_id)

        equ_types = EquipmentType.objects.all().order_by('-add_time')

        # 筛除超级用户
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

        return render(request, 'equipment/edit.html', {
            'equ': equ,
            'equ_types': equ_types,
            'staffs': staffs,
            'type': 'edit'
        })


# 设备申请
class ApplyView(View):
    def get(self, request):
        return render(request, 'equipment/apply.html')


# 设备审核
class VerifyView(View):
    def get(self, request):
        return render(request, 'equipment/verify.html')
