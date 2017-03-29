# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from equipments.models import Equipment, EquipmentType
from operation.models import EquipmentApply, EquipmentStaff, EquipmentPerson
from users.models import UserProfile


# 设备浏览 GET
class ListView(View):
    def get(self, request):

        # 获取所有设备信息，根据添加时间排序
        equs = Equipment.objects.all().order_by('-add_time')

        return render(request, 'equipment/list.html', {
            'equs': equs
        })


# 设备领用 GET
class UseView(View):
    def get(self, request, equ_id):

        # 通过 equ_id 获取当前设备信息
        equ = Equipment.objects.get(id=equ_id)

        return render(request, 'equipment/use.html', {
            'equ': equ
        })


# 设备领用 POST
class UseEquView(View):
    def post(self, request):

        # 获取表单信息
        equ_id = request.POST.get('equi_id', '')
        person_id = request.POST.get('person_id', '')
        use_date = request.POST.get('use_date', '')
        revert_date = request.POST.get('revert_date', '')
        remark = request.POST.get('remark', '')

        # 初始化 设备申请 信息
        equ_apply = EquipmentApply()
        equ_apply.equipment = Equipment.objects.get(id=equ_id)
        equ_apply.person = UserProfile.objects.get(id=person_id)
        equ_apply.type = '0'
        equ_apply.status = '0'
        equ_apply.use_date = use_date
        equ_apply.revert_date = revert_date
        equ_apply.remark = remark
        equ_apply.save()

        # 获取当前用户
        staff = UserProfile.objects.get(id=request.user.id)
        # 获取当前用户的 设备申请 信息
        equ_applys = EquipmentApply.objects.filter(person=staff).order_by('-add_time')

        # 转到 设备申请 页面
        return render(request, 'equipment/apply.html', {
            'equ_applys': equ_applys,
            'staff': staff
        })


# 设备归还 GET
class RevertView(View):
    def get(self, request):

        # 获取当前用户
        staff = UserProfile.objects.get(id=request.user.id)

        # 获取设备保管人为当前用户的 设备信息
        equs = EquipmentStaff.objects.filter(person=staff)

        return render(request, 'equipment/revert.html', {
            'equs': equs
        })


# 设备归还 Ajax
class RevertEquView(View):
    def post(self, request):

        # 获取表单信息
        # 根据 equ_id 获取 设备信息

        return HttpResponse('{"status":"success","msg":"归还申请提交成功"}', content_type='application/json')


# 设备资料 GET
class InfoView(View):
    def get(self, request):

        # 获取所有设备信息，根据添加时间排序
        equs = Equipment.objects.all().order_by('-add_time')

        return render(request, 'equipment/info.html', {
            'equs': equs
        })


# 添加设备 GET POST
class AddView(View):
    def get(self, request):

        # 获取所有 设备类型 信息，根据添加时间排序
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

        # 获取表单信息
        equi_name = request.POST.get('equi_name', '')
        equi_type_id = request.POST.get('equi_type', '')
        equi_person_id = request.POST.get('equi_person', '')
        equi_num = request.POST.get('equi_num', '')
        equi_status = request.POST.get('equi_status', '')
        effect_date = request.POST.get('effect_date', '')
        equi_money = request.POST.get('equi_money', '')
        buy_date = request.POST.get('buy_date', '')
        remark = request.POST.get('remark', '')

        # 初始化 设备信息
        equipment = Equipment()
        equipment.equi_type = EquipmentType.objects.get(id=equi_type_id)
        equipment.equi_name = equi_name
        equipment.equi_num = equi_num
        equipment.equi_status = equi_status
        equipment.effect_date = effect_date
        equipment.equi_money = equi_money
        equipment.buy_date = buy_date
        equipment.remark = remark
        # 设置为 未领用
        equipment.use_status = '0'
        equipment.save()

        # 初始化 设备负责人
        equipment_person = EquipmentPerson()
        equipment_person.equipment = equipment
        equipment_person.person = UserProfile.objects.get(id=equi_person_id)
        equipment_person.save()

        # 获取所有设备信息，根据添加时间排序
        equs = Equipment.objects.all().order_by('-add_time')

        # 转到 设备资料 页面
        return render(request, 'equipment/info.html', {
            'equs': equs
        })


# 编辑设备 GET
class EditView(View):
    def get(self, request, equ_id):

        # 通过 equ_id 获取当前设备信息
        equ = Equipment.objects.get(id=equ_id)

        # 获取所有 设备类型
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


# 编辑设备 Ajax
class EditEquView(View):
    def post(self, request):

        # 获取表单信息
        equi_id = request.POST.get('equi_id', '')
        equi_type_id = request.POST.get('equi_type', '')
        equi_person_id = request.POST.get('equi_person', '')
        equi_name = request.POST.get('equi_name', '')
        equi_num = request.POST.get('equi_num', '')
        equi_status = request.POST.get('equi_status', '')
        effect_date = request.POST.get('effect_date', '')
        equi_money = request.POST.get('equi_money', '')
        buy_date = request.POST.get('buy_date', '')
        remark = request.POST.get('remark', '')

        # 更改 设备信息
        equipment = Equipment.objects.get(id=equi_id)
        equipment.equi_type = EquipmentType.objects.get(id=equi_type_id)
        equipment.equi_name = equi_name
        equipment.equi_num = equi_num
        equipment.equi_status = equi_status
        equipment.effect_date = effect_date
        equipment.equi_money = equi_money
        equipment.buy_date = buy_date
        equipment.remark = remark
        equipment.save()

        # 更改 设备负责人 信息
        equipment_person = EquipmentPerson.objects.get(equipment=equipment)
        equipment_person.person = UserProfile.objects.get(id=equi_person_id)
        equipment_person.save()

        # 初始化 设备变更记录
        # equ_change = EquipmentChange()
        # equ_change.equipment = equipment
        # equ_change.equi_type = equipment.equi_type.name
        # equ_change.equi_person = equipment.equi_person.name
        # equ_change.equi_num = equipment.equi_num
        # equ_change.equi_status = equipment.equi_status
        # equ_change.effect_date = equipment.effect_date
        # equ_change.equi_money = equipment.equi_money
        # equ_change.buy_date = equipment.buy_date
        # equ_change.remark = equipment.remark
        # equ_change.save()

        return HttpResponse('{"status":"success","msg":"编辑设备资料成功"}', content_type='application/json')


# 设备申请 GET
class ApplyView(View):
    def get(self, request):

        # 获取当前用户
        staff = UserProfile.objects.get(id=request.user.id)

        # 获取当前用户的 设备申请 信息
        equ_applys = EquipmentApply.objects.filter(person=staff).order_by('-add_time')

        return render(request, 'equipment/apply.html', {
            'equ_applys': equ_applys,
            'staff': staff
        })


# 设备审核 GET
class VerifyView(View):
    def get(self, request):

        # 获取当前用户
        staff = UserProfile.objects.get(id=request.user.id)

        # 设备负责人 为当前用户
        equ_applys = EquipmentPerson.objects.filter(person=staff)

        return render(request, 'equipment/verify.html', {
            'equ_applys': equ_applys
        })


# 同意领用 Ajax
class AgreeEquView(View):
    def post(self, request):

        # 获取表单信息
        equ_apply_id = request.POST.get('equ_apply_id', '')

        # 修改 设备申请 相关信息
        equ_apply = EquipmentApply.objects.get(id=equ_apply_id)
        equ_apply.status = '1'
        equ_apply.save()

        # 修改设备相关信息
        equ = equ_apply.equipment
        equ.use_status = '1'
        equ.use_person = equ_apply.person
        equ.use_date = equ_apply.use_date
        equ.revert_date = equ_apply.revert_date
        equ.save()

        return HttpResponse('{"status":"success","msg":"同意设备领用申请操作成功"}', content_type='application/json')


# 拒绝领用 Ajax
class RefuseEquView(View):
    def post(self, request):

        # 获取表单信息
        equ_apply_id = request.POST.get('equ_apply_id', '')

        # 修改设备申请相关信息
        equ_apply = EquipmentApply.objects.get(id=equ_apply_id)
        equ_apply.status = '2'
        equ_apply.save()

        return HttpResponse('{"status":"success","msg":"拒绝设备领用申请操作成功"}', content_type='application/json')
