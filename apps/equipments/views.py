# coding:utf-8
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from equipments.models import Equipment, EquipmentType
from operation.models import EquipmentApply
from users.models import UserProfile


# 设备浏览 GET
class ListView(View):
    def get(self, request):
        equs = Equipment.objects.all()

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            equs = equs.filter(Q(equ_name__icontains=search_keywords) |
                               Q(id__icontains=search_keywords) |
                               Q(equ_type_name__icontains=search_keywords) |
                               Q(file_num__icontains=search_keywords) |
                               Q(equ_staff__icontains=search_keywords) |
                               Q(equ_num__icontains=search_keywords) |
                               Q(equ_status__icontains=search_keywords) |
                               # 不可搜索日期
                               # Q(effect_date__icontains=search_keywords) |
                               Q(equ_money__icontains=search_keywords) |
                               Q(equ_person__icontains=search_keywords))

        # 排序
        if category == 'equ_id' and mode == 'positive':
            equs = equs.order_by('id')
        elif category == 'equ_id' and mode == 'negative':
            equs = equs.order_by('-id')
        elif category == 'use_date' and mode == 'positive':
            equs = equs.order_by('use_date')
        elif category == 'use_date' and mode == 'negative':
            equs = equs.order_by('-use_date')
        elif category == 'revert_date' and mode == 'positive':
            equs = equs.order_by('revert_date')
        elif category == 'revert_date' and mode == 'negative':
            equs = equs.order_by('-revert_date')
        elif category == 'add_time' and mode == 'positive':
            equs = equs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            equs = equs.order_by('-add_time')

        return render(request, 'equipment/list.html', {
            'equs': equs
        })


# 设备资料 GET
class InfoView(View):
    def get(self, request):
        equs = Equipment.objects.all()

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            equs = equs.filter(Q(equ_name__icontains=search_keywords) |
                               Q(id__icontains=search_keywords) |
                               Q(equ_type_name__icontains=search_keywords) |
                               Q(file_num__icontains=search_keywords) |
                               Q(equ_staff__icontains=search_keywords) |
                               Q(equ_num__icontains=search_keywords) |
                               Q(equ_status__icontains=search_keywords) |
                               Q(equ_money__icontains=search_keywords) |
                               Q(equ_person__icontains=search_keywords))

        # 排序
        if category == 'equ_id' and mode == 'positive':
            equs = equs.order_by('id')
        elif category == 'equ_id' and mode == 'negative':
            equs = equs.order_by('-id')
        elif category == 'use_date' and mode == 'positive':
            equs = equs.order_by('use_date')
        elif category == 'use_date' and mode == 'negative':
            equs = equs.order_by('-use_date')
        elif category == 'revert_date' and mode == 'positive':
            equs = equs.order_by('revert_date')
        elif category == 'revert_date' and mode == 'negative':
            equs = equs.order_by('-revert_date')
        elif category == 'add_time' and mode == 'positive':
            equs = equs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            equs = equs.order_by('-add_time')

        return render(request, 'equipment/info.html', {
            'equs': equs
        })


# 添加设备 GET POST
class AddView(View):
    def get(self, request):

        # 设备类型 信息
        equ_types = EquipmentType.objects.all().order_by('-add_time')

        # 筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        return render(request, 'equipment/edit.html', {
            'equ_types': equ_types,
            'staffs': staffs,
            'type': 'add'
        })

    def post(self, request):

        # 获取表单信息
        equ_name = request.POST.get('equ_name', '')
        file_num = request.POST.get('file_num', '')
        equ_type_id = request.POST.get('equ_type_id', '')
        equ_person_id = request.POST.get('equ_person_id', '')
        equ_num = request.POST.get('equ_num', '')
        equ_status = request.POST.get('equ_status', '')
        effect_date = request.POST.get('effect_date', '')
        equ_money = request.POST.get('equ_money', '')
        buy_date = request.POST.get('buy_date', '')
        remark = request.POST.get('remark', '')

        # 初始化 设备信息
        equipment = Equipment()
        if equ_type_id:
            equipment.equ_type_id = equ_type_id
            equipment.equ_type_name = EquipmentType.objects.get(id=equ_type_id)
        if equ_person_id:
            equipment.equ_person_id = equ_person_id  # 设备负责人信息
            equipment.equ_person = UserProfile.objects.get(id=equ_person_id).name
        equipment.equ_name = equ_name
        equipment.file_num = file_num
        equipment.equ_num = equ_num
        equipment.equ_status = equ_status
        equipment.effect_date = effect_date
        equipment.equ_money = equ_money
        equipment.buy_date = buy_date
        equipment.remark = remark

        equipment.use_status = '未领用'  # 使用状态为 未领用
        equipment.equ_staff_id = None  # 设备保管人信息
        equipment.equ_staff = None
        equipment.use_date = None  # 领用时间
        equipment.revert_date = None  # 归还时间
        equipment.save()

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
        equ = Equipment.objects.get(id=int(equ_id))

        # 获取所有 设备类型
        equ_types = EquipmentType.objects.all().order_by('-add_time')

        # 筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

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
        equ_id = request.POST.get('equ_id', '')
        equ_name = request.POST.get('equ_name', '')
        if not equ_name:
            return HttpResponse('{"status":"success","msg":"请填写设备名称"}', content_type='application/json')
        file_num = request.POST.get('file_num', '')
        equ_type_id = request.POST.get('equ_type_id', '')
        equ_person_id = request.POST.get('equ_person_id', '')
        equ_num = request.POST.get('equ_num', '')
        equ_status = request.POST.get('equ_status', '')
        effect_date = request.POST.get('effect_date', '')
        equ_money = request.POST.get('equ_money', '')
        buy_date = request.POST.get('buy_date', '')
        remark = request.POST.get('remark', '')

        # 更改 设备信息
        equipment = Equipment.objects.get(id=equ_id)
        if equ_type_id:
            equipment.equ_type_id = equ_type_id
            equipment.equ_type_name = EquipmentType.objects.get(id=equ_type_id).name
        if equ_person_id:
            equipment.equ_person_id = equ_person_id
            equipment.equ_person = UserProfile.objects.get(id=equ_person_id).name
        equipment.equ_name = equ_name
        equipment.equ_num = equ_num
        equipment.file_num = file_num
        equipment.equ_status = equ_status
        equipment.effect_date = effect_date
        equipment.equ_money = equ_money
        equipment.buy_date = buy_date
        equipment.remark = remark
        equipment.save()

        return HttpResponse('{"status":"success","msg":"编辑设备资料成功"}', content_type='application/json')


# 设备领用 GET
class UseView(View):
    def get(self, request, equ_id):
        # 通过 equ_id 获取当前设备信息
        equ = Equipment.objects.get(id=int(equ_id))

        return render(request, 'equipment/use.html', {
            'equ': equ
        })


# 设备领用 POST
class UseEquView(View):
    def post(self, request):
        # 获取表单信息
        equ_id = request.POST.get('equ_id', '')
        person_id = request.POST.get('person_id', '')
        equipment_person_id = request.POST.get('equipment_person_id', '')
        equ_status = request.POST.get('equ_status', '')
        use_date = request.POST.get('use_date', '')
        revert_date = request.POST.get('revert_date', '')
        remark = request.POST.get('remark', '')

        # 初始化 设备申请 信息
        equ_apply = EquipmentApply()
        equ_apply.equipment_id = equ_id
        equ_apply.equipment_name = Equipment.objects.get(id=equ_id)
        equ_apply.person_id = person_id
        equ_apply.person_name = UserProfile.objects.get(id=person_id)
        # 设备状态为 正常 时，才将它送往 设备负责人 处审核；否则送往 系统管理员
        if equ_status == '正常':
            equ_apply.equipment_person_id = equipment_person_id
            equ_apply.equipment_person = UserProfile.objects.get(id=equipment_person_id)
        else:
            equ_apply.equipment_person_id = None
            equ_apply.equipment_person = None
        equ_apply.type = '领用'  # 申请类型为 领用
        equ_apply.status = '审核中'  # 审核状态为 审核中
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


# 设备申请 GET
class ApplyView(View):
    def get(self, request):
        # 获取当前用户的 设备申请 信息
        equ_applys = EquipmentApply.objects.filter(person_id=request.user.id).order_by('-add_time')

        return render(request, 'equipment/apply.html', {
            'equ_applys': equ_applys
        })


# 设备审核 GET
class VerifyView(View):
    def get(self, request):

        # 系统管理员 审核设备状态为 限制使用 的设备，限制使用的设备在领用时设置了 equipment_person_id=None
        if request.user.permission == '系统管理员':
            equ_applys = EquipmentApply.objects.filter(
                Q(equipment_person_id=request.user.id) | Q(equipment_person_id=None))
        else:
            equ_applys = EquipmentApply.objects.filter(equipment_person_id=request.user.id)

        return render(request, 'equipment/verify.html', {
            'equ_applys': equ_applys
        })


# 同意领用 Ajax
class AgreeEquView(View):
    def post(self, request):

        # 获取表单信息
        equ_apply_id = request.POST.get('equ_apply_id', '')

        # 获取 设备申请 信息
        equ_apply = EquipmentApply.objects.get(id=equ_apply_id)

        # 申请类型为 领用
        if equ_apply.type == '领用':
            # 修改 设备申请 相关信息
            equ_apply.status = '审核通过'  # 设备状态修改为 审核通过
            equ_apply.save()

            # 审核通过，修改设备相关信息
            equ = equ_apply.equipment
            equ.use_status = '已领用'  # 设备使用状态设为 已领用
            equ.equ_staff_id = equ_apply.person_id  # 设备保管人
            equ.equ_staff = UserProfile.objects.get(id=equ_apply.person_id).name
            equ.use_date = equ_apply.use_date  # 将设备申请中的信息放入设备信息中
            equ.revert_date = equ_apply.revert_date
            equ.save()

            return HttpResponse('{"status":"success","msg":"同意设备领用申请操作成功"}', content_type='application/json')

        # 申请类型为 归还
        elif equ_apply.type == '归还':
            # 修改 设备申请 相关信息
            equ_apply.status = '审核通过'  # 设备状态修改为 审核通过
            equ_apply.save()

            # 审核通过，修改设备相关信息
            equ = equ_apply.equipment
            equ.use_status = '未领用'  # 设备使用状态设为 未领用
            equ.equ_staff_id = None  # 删除 设备保管人 中的信息
            equ.equ_staff = None
            equ.use_date = None  # 删除设备信息中的 领用时间
            equ.revert_date = None  # 删除设备信息中的 归还时间
            equ.save()

            return HttpResponse('{"status":"success","msg":"同意设备归还申请操作成功"}', content_type='application/json')


# 拒绝领用 Ajax
class RefuseEquView(View):
    def post(self, request):

        # 获取表单信息
        equ_apply_id = request.POST.get('equ_apply_id', '')

        # 获取 设备申请 信息
        equ_apply = EquipmentApply.objects.get(id=equ_apply_id)

        # 申请类型为 领用
        if equ_apply.type == '领用':
            # 修改设备申请相关信息
            equ_apply.status = '审核未通过'  # 设备状态修改为 审核未通过
            equ_apply.save()
            return HttpResponse('{"status":"success","msg":"拒绝设备领用申请操作成功"}', content_type='application/json')

        # 申请类型为 归还
        elif equ_apply.type == '归还':
            # 修改设备申请相关信息
            equ_apply.status = '审核未通过'  # 设备状态修改为 审核未通过
            equ_apply.save()
            return HttpResponse('{"status":"success","msg":"拒绝设备归还申请操作成功"}', content_type='application/json')


# 设备归还 GET
class RevertView(View):
    def get(self, request):
        # 获取设备保管人为当前用户的 设备信息
        equs = Equipment.objects.filter(equ_staff_id=request.user.id)

        return render(request, 'equipment/revert.html', {
            'equs': equs
        })


# 设备归还 Ajax
class RevertEquView(View):
    def post(self, request):
        # 获取表单信息
        equ_id = request.POST.get('equ_id', '')
        person_id = request.POST.get('person_id', '')
        equipment_person_id = request.POST.get('equipment_person_id', '')
        use_date = request.POST.get('use_date', '')
        revert_date = request.POST.get('revert_date', '')

        # 初始化 设备申请 信息
        equ_apply = EquipmentApply()
        equ_apply.equipment_id = equ_id
        equ_apply.person_id = person_id
        equ_apply.equipment_person_id = equipment_person_id  # 设备负责人id
        equ_apply.type = '归还'  # 申请类型为 归还
        equ_apply.status = '审核中'  # 审核状态为 审核中
        equ_apply.use_date = use_date
        equ_apply.revert_date = revert_date
        equ_apply.save()

        return HttpResponse('{"status":"success","msg":"归还申请提交成功"}', content_type='application/json')
