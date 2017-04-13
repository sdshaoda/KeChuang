# coding:utf-8
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from equipments.models import Equipment
from operation.models import ProjectApply, ProjectAttendance, ProjectMember, ProjectEquipment
from users.models import UserProfile, Department
from .models import Project, ProjectType, ProjectStage


# 工程浏览 GET
class ListView(View):
    def get(self, request):

        # 检测员 浏览自己为 项目成员 的工程，包括了自己是 工程负责人
        if request.user.permission == '检测员':
            pro_members = ProjectMember.objects.filter(person_id=request.user.id).order_by('-add_time')
            pros = []
            for pro_member in pro_members:
                # 排除已被删除，或者添加未审核的
                if pro_member.project.is_active == 1:
                    pros.append(pro_member.project)

        # 部门负责 浏览负责人为本部门员工 OR 自己为项目成员
        elif request.user.permission == '部门负责':
            pro_members = ProjectMember.objects.filter(
                Q(department_id=request.user.department_id) | Q(person_id=request.user.id)).order_by('-add_time')
            pros = []
            for pro_member in pro_members:
                if pro_member.project.is_active == 1:
                    pros.append(pro_member.project)

        # 公司负责 浏览所有工程
        elif request.user.permission == '公司负责':
            pros = Project.objects.filter(is_active=1).order_by('-add_time')
        else:
            pros = []

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            pros = pros.filter(Q(pro_type_name__icontains=search_keywords) |
                               Q(pro_stage_name__icontains=search_keywords) |
                               Q(id__icontains=search_keywords) |
                               Q(pro_name__icontains=search_keywords) |
                               Q(pro_person__icontains=search_keywords) |
                               Q(department__icontains=search_keywords) |
                               Q(wt_person__icontains=search_keywords) |
                               Q(ht_person__icontains=search_keywords) |
                               Q(ht_name__icontains=search_keywords) |
                               Q(ht_num__icontains=search_keywords) |
                               Q(ht_money__icontains=search_keywords) |
                               Q(js_money__icontains=search_keywords) |
                               Q(wt_dw__icontains=search_keywords) |
                               Q(mobile__icontains=search_keywords) |
                               Q(pro_address__icontains=search_keywords) |
                               Q(remark__icontains=search_keywords))

        # 排序
        if category == 'pro_id' and mode == 'positive':
            pros = pros.order_by('id')
        elif category == 'pro_id' and mode == 'negative':
            pros = pros.order_by('-id')
        elif category == 'pro_person_id' and mode == 'positive':
            pros = pros.order_by('pro_person_id')
        elif category == 'pro_person_id' and mode == 'negative':
            pros = pros.order_by('-pro_person_id')
        elif category == 'department_id' and mode == 'positive':
            pros = pros.order_by('department_id')
        elif category == 'department_id' and mode == 'negative':
            pros = pros.order_by('-department_id')
        elif category == 'wt_person_id' and mode == 'positive':
            pros = pros.order_by('wt_person_id')
        elif category == 'wt_person_id' and mode == 'negative':
            pros = pros.order_by('-wt_person_id')
        elif category == 'ht_person_id' and mode == 'positive':
            pros = pros.order_by('ht_person_id')
        elif category == 'ht_person_id' and mode == 'negative':
            pros = pros.order_by('-ht_person_id')
        elif category == 'ht_num' and mode == 'positive':
            pros = pros.order_by('ht_num')
        elif category == 'ht_num' and mode == 'negative':
            pros = pros.order_by('-ht_num')
        elif category == 'ht_money' and mode == 'positive':
            pros = pros.order_by('ht_money')
        elif category == 'ht_money' and mode == 'negative':
            pros = pros.order_by('-ht_money')
        elif category == 'js_money' and mode == 'positive':
            pros = pros.order_by('js_money')
        elif category == 'js_money' and mode == 'negative':
            pros = pros.order_by('-js_money')
        elif category == 'mobile' and mode == 'positive':
            pros = pros.order_by('mobile')
        elif category == 'mobile' and mode == 'negative':
            pros = pros.order_by('-mobile')
        elif category == 'sign_date' and mode == 'positive':
            pros = pros.order_by('sign_date')
        elif category == 'sign_date' and mode == 'negative':
            pros = pros.order_by('-sign_date')
        elif category == 'start_date' and mode == 'positive':
            pros = pros.order_by('start_date')
        elif category == 'start_date' and mode == 'negative':
            pros = pros.order_by('-start_date')
        elif category == 'finish_date' and mode == 'positive':
            pros = pros.order_by('finish_date')
        elif category == 'finish_date' and mode == 'negative':
            pros = pros.order_by('-finish_date')
        elif category == 'add_time' and mode == 'positive':
            pros = pros.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            pros = pros.order_by('-add_time')

        return render(request, 'project/list.html', {
            'pros': pros
        })


# 工程详情 GET
class DetailView(View):
    def get(self, request, pro_id):
        # 根据 URL 中的 pro_id 获取工程详情
        pro = Project.objects.get(id=int(pro_id))

        # 筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        # 工程类型
        pro_types = ProjectType.objects.all()

        # 项目阶段
        pro_stages = ProjectStage.objects.all()

        pro_members = ProjectMember.objects.filter(project_id=pro_id)
        pro_equs = ProjectEquipment.objects.filter(project_id=pro_id)

        return render(request, 'project/detail.html', {
            'pro': pro,
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages,
            'pro_members': pro_members,
            'pro_equs': pro_equs
        })


# 添加工程 GET POST
class AddProView(View):
    def get(self, request):

        # 用户 列表，筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        # 工程类型
        pro_types = ProjectType.objects.all()

        # 项目阶段
        pro_stages = ProjectStage.objects.all()

        # 除 公司负责 外，其余人只能添加或编辑本部门工程
        if request.user.permission == '公司负责':
            departments = Department.objects.filter(is_department=1)
        else:
            departments = Department.objects.filter(id=request.user.department.id)

        return render(request, 'project/add.html', {
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages,
            'departments': departments
        })

    def post(self, request):
        # 获取表单信息
        pro_name = request.POST.get('pro_name', '')
        pro_type_id = request.POST.get('pro_type_id', '')
        pro_stage_id = request.POST.get('pro_stage_id', '')
        department_id = request.POST.get('department_id', '')
        pro_person_id = request.POST.get('pro_person_id', '')
        wt_person_id = request.POST.get('wt_person_id', '')
        ht_person_id = request.POST.get('ht_person_id', '')

        ht_name = request.POST.get('ht_name', '')
        ht_num = request.POST.get('ht_num', '')
        ht_money = request.POST.get('ht_money', '')
        js_money = request.POST.get('js_money', '')
        wt_dw = request.POST.get('wt_dw', '')
        mobile = request.POST.get('mobile', '')
        pro_address = request.POST.get('pro_address', '')
        sign_date = request.POST.get('sign_date', '')
        start_date = request.POST.get('start_date', '')
        finish_date = request.POST.get('finish_date', '')
        ht_scan = request.FILES.get('ht_scan', '')
        remark = request.POST.get('remark', '')

        if request.user.permission == '公司负责':
            # 直接新建 工程
            project = Project()
            project.is_active = 1  # 工程状态为 有效
            project.pro_name = pro_name
            if pro_type_id:
                project.pro_type_id = pro_type_id
                project.pro_type_name = ProjectType.objects.get(id=pro_type_id)
            if pro_stage_id:
                project.pro_stage_id = pro_stage_id
                project.pro_stage_name = ProjectStage.objects.get(id=pro_stage_id)
            if pro_person_id:
                project.pro_person_id = pro_person_id
                project.pro_person = UserProfile.objects.get(id=pro_person_id).name
            if department_id:
                project.department_id = department_id
                project.department = Department.objects.get(id=department_id).name
            if wt_person_id:
                project.wt_person_id = wt_person_id
                project.wt_person = UserProfile.objects.get(id=wt_person_id).name
            if ht_person_id:
                project.ht_person_id = ht_person_id
                project.ht_person = UserProfile.objects.get(id=ht_person_id).name

            project.ht_name = ht_name
            project.ht_num = ht_num
            project.ht_money = ht_money
            project.js_money = js_money
            project.wt_dw = wt_dw
            project.mobile = mobile
            project.pro_address = pro_address
            if sign_date:
                project.sign_date = sign_date
            if start_date:
                project.start_date = start_date
            if finish_date:
                project.finish_date = finish_date
            project.ht_scan = ht_scan
            project.remark = remark
            project.save()

            # 新建 工程项目成员 信息，且设为 负责人
            pro_member = ProjectMember()
            pro_member.is_pro_person = 1  # 设为 负责人
            pro_member.project_id = project.id
            pro_member.project_name = project.pro_name
            pro_member.person_id = project.pro_person_id
            pro_member.person_name = project.pro_person
            pro_member.department_id = project.department_id
            pro_member.department = project.department
            pro_member.save()
        else:
            # 非 公司负责 权限，初始化 空 工程。 审核通过 后在 工程 中填入相应信息；审核未通过 则删除
            project = Project()
            project.is_active = 0  # 工程状态为 无效
            project.pro_name = pro_name  # 保存必要的信息
            if pro_person_id:
                project.pro_person_id = pro_person_id
                project.pro_person = UserProfile.objects.get(id=pro_person_id).name
            project.save()

        # 初始化 工程申请
        pro_apply = ProjectApply()
        pro_apply.project = project
        pro_apply.project_name = project.pro_name
        pro_apply.person_id = request.user.id
        pro_apply.person_name = request.user.name

        pro_apply.type = '添加工程'
        if request.user.permission == '检测员':
            pro_apply.status = '部门主任审核中'
        if request.user.permission == '部门负责':
            pro_apply.status = '公司领导审核中'
        if request.user.permission == '公司负责':
            pro_apply.status = '审核通过'  # 变更记录的筛选条件

        if pro_type_id:
            pro_apply.pro_type_id = pro_type_id
            pro_apply.pro_type = ProjectType.objects.get(id=pro_type_id).name
        if pro_stage_id:
            pro_apply.pro_stage_id = pro_stage_id
            pro_apply.pro_stage = ProjectStage.objects.get(id=pro_stage_id).name
        if pro_person_id:
            pro_apply.pro_person_id = pro_person_id
            pro_apply.pro_person = UserProfile.objects.get(id=pro_person_id).name
        if department_id:
            pro_apply.department_id = department_id
            pro_apply.department = Department.objects.get(id=department_id).name
        if wt_person_id:
            pro_apply.wt_person_id = wt_person_id
            pro_apply.wt_person = UserProfile.objects.get(id=wt_person_id).name
        if ht_person_id:
            pro_apply.ht_person_id = ht_person_id
            pro_apply.ht_person = UserProfile.objects.get(id=ht_person_id).name

        pro_apply.ht_name = ht_name
        pro_apply.ht_num = ht_num
        pro_apply.ht_money = ht_money
        pro_apply.js_money = js_money
        pro_apply.wt_dw = wt_dw
        pro_apply.mobile = mobile
        pro_apply.pro_address = pro_address
        if sign_date:
            pro_apply.sign_date = sign_date
        if start_date:
            pro_apply.start_date = start_date
        if finish_date:
            pro_apply.finish_date = finish_date
        pro_apply.ht_scan = ht_scan
        pro_apply.remark = remark
        pro_apply.save()

        # 申请人 为当前用户的申请
        pro_applys = ProjectApply.objects.filter(person_id=request.user.id).order_by('-add_time')
        # 转到 工程申请
        return render(request, 'project/apply.html', {
            'pro_applys': pro_applys
        })


# 编辑工程 GET
class EditView(View):
    def get(self, request, pro_id):
        # 根据 URL 中的 pro_id 获取工程详情
        pro = Project.objects.get(id=int(pro_id))

        # 筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        # 工程类型
        pro_types = ProjectType.objects.all()

        # 项目阶段
        pro_stages = ProjectStage.objects.all()

        # 除 公司负责 外，其余人只能添加或编辑本部门工程
        if request.user.permission == '公司负责':
            departments = Department.objects.filter(is_department=1)
        else:
            departments = Department.objects.filter(id=request.user.department.id)

        # 如果是 工程负责人 或 公司负责 ，能够直接添加 工程项目成员 和 工程设备
        if pro.pro_person_id == request.user.id or request.user.permission == '公司负责':
            is_permit = 1
        else:
            is_permit = 0

        pro_members = ProjectMember.objects.filter(project_id=pro_id)
        pro_equs = ProjectEquipment.objects.filter(project_id=pro_id)
        equs = Equipment.objects.all()

        return render(request, 'project/edit.html', {
            'pro': pro,
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages,
            'departments': departments,
            'is_permit': is_permit,
            'pro_members': pro_members,
            'equs': equs,
            'pro_equs': pro_equs
        })


# 编辑工程 POST
class EditProView(View):
    def post(self, request):

        # 获取表单信息
        pro_id = request.POST.get('pro_id', '')
        pro_name = request.POST.get('pro_name', '')
        department_id = request.POST.get('department_id', '')
        pro_person_id = request.POST.get('pro_person_id', '')
        pro_type_id = request.POST.get('pro_type_id', '')
        pro_stage_id = request.POST.get('pro_stage_id', '')
        wt_person_id = request.POST.get('wt_person_id', '')
        ht_person_id = request.POST.get('ht_person_id', '')

        ht_name = request.POST.get('ht_name', '')
        ht_num = request.POST.get('ht_num', '')
        ht_money = request.POST.get('ht_money', '')
        js_money = request.POST.get('js_money', '')
        wt_dw = request.POST.get('wt_dw', '')
        mobile = request.POST.get('mobile', '')
        pro_address = request.POST.get('pro_address', '')
        sign_date = request.POST.get('sign_date', '')
        start_date = request.POST.get('start_date', '')
        finish_date = request.POST.get('finish_date', '')
        ht_scan = request.FILES.get('ht_scan', '')
        remark = request.POST.get('remark', '')

        project = Project.objects.get(id=pro_id)

        # 公司负责 直接修改 工程 信息，但要生成 审核通过 的 工程申请
        if request.user.permission == '公司负责':
            # 修改了 工程负责人
            if pro_person_id != project.pro_person_id:
                # 删除原有的 工程负责人 信息
                old_pro_member = ProjectMember.objects.get(is_pro_person=1)
                old_pro_member.delete()
                # 新建 工程项目成员 信息，且设为 负责人
                pro_member = ProjectMember()
                pro_member.is_pro_person = 1  # 设为 负责人
                pro_member.project_id = project.id
                pro_member.project_name = pro_name
                if pro_person_id:
                    pro_member.person_id = pro_person_id
                    pro_member.person_name = UserProfile.objects.get(id=pro_person_id).name
                if department_id:
                    pro_member.department_id = department_id
                    pro_member.department = Department.objects.get(id=department_id).name
                pro_member.save()

            project.pro_name = pro_name
            if pro_type_id:
                project.pro_type_id = pro_type_id
                project.pro_type_name = ProjectType.objects.get(id=pro_type_id)
            if pro_stage_id:
                project.pro_stage_id = pro_stage_id
                project.pro_stage_name = ProjectStage.objects.get(id=pro_stage_id)
            if pro_person_id:
                project.pro_person_id = pro_person_id
                project.pro_person = UserProfile.objects.get(id=pro_person_id).name
            if department_id:
                project.department_id = department_id
                project.department = Department.objects.get(id=department_id).name
            if wt_person_id:
                project.wt_person_id = wt_person_id
                project.wt_person = UserProfile.objects.get(id=wt_person_id).name
            if ht_person_id:
                project.ht_person_id = ht_person_id
                project.ht_person = UserProfile.objects.get(id=ht_person_id).name

            project.ht_name = ht_name
            project.ht_num = ht_num
            project.ht_money = ht_money
            project.js_money = js_money
            project.wt_dw = wt_dw
            project.mobile = mobile
            project.pro_address = pro_address
            # 不写判断会报错
            if sign_date:
                project.sign_date = sign_date
            else:
                project.sign_date = None
            if start_date:
                project.start_date = start_date
            else:
                project.start_date = None
            if finish_date:
                project.finish_date = finish_date
            else:
                project.finish_date = None
            # 上传文件才修改原有值，否则不修改
            if ht_scan:
                project.ht_scan = ht_scan
            project.remark = remark
            project.save()

        # 初始化 工程申请
        pro_apply = ProjectApply()
        pro_apply.project = project
        pro_apply.project_name = project.pro_name
        pro_apply.person_id = request.user.id
        pro_apply.person_name = request.user.name

        pro_apply.type = '修改信息'
        if request.user.permission == '检测员':
            pro_apply.status = '部门主任审核中'
        if request.user.permission == '部门负责':
            pro_apply.status = '公司领导审核中'
        if request.user.permission == '公司负责':
            pro_apply.status = '审核通过'  # 变更记录的筛选条件

        if pro_type_id:
            pro_apply.pro_type_id = pro_type_id
            pro_apply.pro_type = ProjectType.objects.get(id=pro_type_id).name
        if pro_stage_id:
            pro_apply.pro_stage_id = pro_stage_id
            pro_apply.pro_stage = ProjectStage.objects.get(id=pro_stage_id).name
        if pro_person_id:
            pro_apply.pro_person_id = pro_person_id
            pro_apply.pro_person = UserProfile.objects.get(id=pro_person_id).name
        if department_id:
            pro_apply.department_id = department_id
            pro_apply.department = Department.objects.get(id=department_id).name
        if wt_person_id:
            pro_apply.wt_person_id = wt_person_id
            pro_apply.wt_person = UserProfile.objects.get(id=wt_person_id).name
        if ht_person_id:
            pro_apply.ht_person_id = ht_person_id
            pro_apply.ht_person = UserProfile.objects.get(id=ht_person_id).name

        pro_apply.ht_name = ht_name
        pro_apply.ht_num = ht_num
        pro_apply.ht_money = ht_money
        pro_apply.js_money = js_money
        pro_apply.wt_dw = wt_dw
        pro_apply.mobile = mobile
        pro_apply.pro_address = pro_address
        if sign_date:
            pro_apply.sign_date = sign_date
        if start_date:
            pro_apply.start_date = start_date
        if finish_date:
            pro_apply.finish_date = finish_date
        pro_apply.ht_scan = ht_scan
        pro_apply.remark = remark
        pro_apply.save()

        # 申请人 为当前用户的申请
        pro_applys = ProjectApply.objects.filter(person_id=request.user.id).order_by('-add_time')
        # 转到 工程申请
        return render(request, 'project/apply.html', {
            'pro_applys': pro_applys
        })


# 删除工程 Ajax
class DeleteView(View):
    def post(self, request):
        pro_id = request.POST.get('pro_id', '')

        project = Project.objects.get(id=int(pro_id))
        # 除 公司负责 外，不对 工程 进行任何操作

        # 初始化 工程申请
        pro_apply = ProjectApply()
        # 删除工程 的 工程申请 只保存基本信息
        pro_apply.project = project
        pro_apply.project_name = project.pro_name
        pro_apply.person_id = request.user.id
        pro_apply.person_name = request.user.name
        pro_apply.type = '删除工程'
        if request.user.permission == '检测员':
            pro_apply.status = '部门主任审核中'
            pro_apply.save()
        if request.user.permission == '部门负责':
            pro_apply.status = '公司领导审核中'
            pro_apply.save()
        if request.user.permission == '公司负责':
            project.is_active = 0  # 工程状态设置为无效，保留在数据库
            project.save()
            pro_apply.status = '审核通过'  # 变更记录的筛选条件
            pro_apply.save()
            return HttpResponse('{"status":"success","msg":"删除工程已成功"}', content_type='application/json')

        if ProjectApply.objects.filter(id=pro_apply.id):
            return HttpResponse('{"status":"success","msg":"删除工程申请已提交"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除工程申请提交失败"}', content_type='application/json')


# 工程申请 GET
class ApplyView(View):
    def get(self, request):
        # 申请人 为当前用户的申请
        pro_applys = ProjectApply.objects.filter(person_id=request.user.id).order_by('-add_time')

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            pro_applys = pro_applys.filter(Q(pro_type__icontains=search_keywords) |
                                           Q(pro_stage__icontains=search_keywords) |
                                           Q(id__icontains=search_keywords) |
                                           Q(type__icontains=search_keywords) |
                                           Q(status__icontains=search_keywords) |
                                           Q(project_name__icontains=search_keywords) |
                                           Q(person_name__icontains=search_keywords) |
                                           Q(pro_person__icontains=search_keywords) |
                                           Q(department__icontains=search_keywords) |
                                           Q(wt_person__icontains=search_keywords) |
                                           Q(ht_person__icontains=search_keywords) |
                                           Q(ht_name__icontains=search_keywords) |
                                           Q(ht_num__icontains=search_keywords) |
                                           Q(ht_money__icontains=search_keywords) |
                                           Q(js_money__icontains=search_keywords) |
                                           Q(wt_dw__icontains=search_keywords) |
                                           Q(mobile__icontains=search_keywords) |
                                           Q(pro_address__icontains=search_keywords) |
                                           Q(remark__icontains=search_keywords))

        # 排序
        if category == 'pro_apply_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('id')
        elif category == 'pro_apply_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-id')
        elif category == 'pro_type_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_type_id')
        elif category == 'pro_type_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_type_id')
        elif category == 'pro_stage_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_stage_id')
        elif category == 'pro_stage_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_stage_id')
        elif category == 'department_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('department_id')
        elif category == 'department_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-department_id')
        elif category == 'pro_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_person_id')
        elif category == 'pro_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_person_id')
        elif category == 'wt_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('wt_person_id')
        elif category == 'wt_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-wt_person_id')
        elif category == 'ht_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_person_id')
        elif category == 'ht_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_person_id')
        elif category == 'ht_num' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_num')
        elif category == 'ht_num' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_num')
        elif category == 'ht_money' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_money')
        elif category == 'ht_money' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_money')
        elif category == 'js_money' and mode == 'positive':
            pro_applys = pro_applys.order_by('js_money')
        elif category == 'js_money' and mode == 'negative':
            pro_applys = pro_applys.order_by('-js_money')
        elif category == 'mobile' and mode == 'positive':
            pro_applys = pro_applys.order_by('mobile')
        elif category == 'mobile' and mode == 'negative':
            pro_applys = pro_applys.order_by('-mobile')
        elif category == 'sign_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('sign_date')
        elif category == 'sign_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-sign_date')
        elif category == 'start_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('start_date')
        elif category == 'start_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-start_date')
        elif category == 'finish_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('finish_date')
        elif category == 'finish_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-finish_date')
        elif category == 'add_time' and mode == 'positive':
            pro_applys = pro_applys.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            pro_applys = pro_applys.order_by('-add_time')

        return render(request, 'project/apply.html', {
            'pro_applys': pro_applys
        })


# 申请详情 GET
class ApplyDetailView(View):
    def get(self, request, pro_apply_id):
        pro_apply = ProjectApply.objects.get(id=int(pro_apply_id))

        # 筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        # 工程类型
        pro_types = ProjectType.objects.all()

        # 项目阶段
        pro_stages = ProjectStage.objects.all()

        return render(request, 'project/apply_detail.html', {
            'pro_apply': pro_apply,
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages
        })


# 工程审核 GET
class VerifyView(View):
    def get(self, request):

        # 部门负责 只接受本部门的申请，且 审核状态 为 部门主任审核中
        if request.user.permission == '部门负责':
            pro_applys = ProjectApply.objects.filter(department=request.user.department.name,
                                                     status='部门主任审核中').order_by('-add_time')
        # 公司负责 接受所有部门的申请，且 审核状态 为 公司领导审核中
        elif request.user.permission == '公司负责':
            pro_applys = ProjectApply.objects.filter(status='公司领导审核中').order_by('-add_time')
        else:
            pro_applys = []

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            pro_applys = pro_applys.filter(Q(pro_type__icontains=search_keywords) |
                                           Q(pro_stage__icontains=search_keywords) |
                                           Q(id__icontains=search_keywords) |
                                           Q(type__icontains=search_keywords) |
                                           Q(status__icontains=search_keywords) |
                                           Q(project_name__icontains=search_keywords) |
                                           Q(person_name__icontains=search_keywords) |
                                           Q(pro_person__icontains=search_keywords) |
                                           Q(department__icontains=search_keywords) |
                                           Q(wt_person__icontains=search_keywords) |
                                           Q(ht_person__icontains=search_keywords) |
                                           Q(ht_name__icontains=search_keywords) |
                                           Q(ht_num__icontains=search_keywords) |
                                           Q(ht_money__icontains=search_keywords) |
                                           Q(js_money__icontains=search_keywords) |
                                           Q(wt_dw__icontains=search_keywords) |
                                           Q(mobile__icontains=search_keywords) |
                                           Q(pro_address__icontains=search_keywords) |
                                           Q(remark__icontains=search_keywords))

        # 排序
        if category == 'pro_apply_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('id')
        elif category == 'pro_apply_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-id')
        elif category == 'pro_type_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_type_id')
        elif category == 'pro_type_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_type_id')
        elif category == 'pro_stage_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_stage_id')
        elif category == 'pro_stage_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_stage_id')
        elif category == 'department_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('department_id')
        elif category == 'department_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-department_id')
        elif category == 'pro_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_person_id')
        elif category == 'pro_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_person_id')
        elif category == 'wt_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('wt_person_id')
        elif category == 'wt_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-wt_person_id')
        elif category == 'ht_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_person_id')
        elif category == 'ht_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_person_id')
        elif category == 'ht_num' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_num')
        elif category == 'ht_num' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_num')
        elif category == 'ht_money' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_money')
        elif category == 'ht_money' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_money')
        elif category == 'js_money' and mode == 'positive':
            pro_applys = pro_applys.order_by('js_money')
        elif category == 'js_money' and mode == 'negative':
            pro_applys = pro_applys.order_by('-js_money')
        elif category == 'mobile' and mode == 'positive':
            pro_applys = pro_applys.order_by('mobile')
        elif category == 'mobile' and mode == 'negative':
            pro_applys = pro_applys.order_by('-mobile')
        elif category == 'sign_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('sign_date')
        elif category == 'sign_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-sign_date')
        elif category == 'start_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('start_date')
        elif category == 'start_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-start_date')
        elif category == 'finish_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('finish_date')
        elif category == 'finish_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-finish_date')
        elif category == 'add_time' and mode == 'positive':
            pro_applys = pro_applys.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            pro_applys = pro_applys.order_by('-add_time')

        return render(request, 'project/verify.html', {
            'pro_applys': pro_applys
        })


# 同意申请 Ajax
class AgreeProView(View):
    def post(self, request):

        pro_apply_id = request.POST.get('pro_apply_id', '')

        pro_apply = ProjectApply.objects.get(id=int(pro_apply_id))
        pro = pro_apply.project

        if request.user.permission == '部门负责':
            # 部门负责 将申请提交给 公司负责
            pro_apply.status = '公司领导审核中'
            pro_apply.save()
            return HttpResponse('{"status":"success","msg":"同意工程申请操作成功，申请转到公司领导审核"}', content_type='application/json')

        elif request.user.permission == '公司负责':
            # 判断 工程申请 的类型
            if pro_apply.type == '添加工程':
                pro.is_active = 1  # 工程状态设置为有效
                # 将 工程申请 中的内容写进 工程 信息
                pro.pro_name = pro_apply.project_name

                pro.pro_type_id = pro_apply.pro_type_id
                pro.pro_type_name = pro_apply.pro_type
                pro.pro_stage_id = pro_apply.pro_stage_id
                pro.pro_stage_name = pro_apply.pro_stage
                pro.department_id = pro_apply.department_id
                pro.department = pro_apply.department
                pro.pro_person_id = pro_apply.pro_person_id
                pro.pro_person = pro_apply.pro_person
                pro.wt_person_id = pro_apply.wt_person_id
                pro.wt_person = pro_apply.wt_person
                pro.ht_person_id = pro_apply.ht_person_id
                pro.ht_person = pro_apply.ht_person

                pro.ht_name = pro_apply.ht_name
                pro.ht_num = pro_apply.ht_num
                pro.ht_money = pro_apply.ht_money
                pro.js_money = pro_apply.js_money
                pro.wt_dw = pro_apply.wt_dw
                pro.mobile = pro_apply.mobile
                pro.pro_address = pro_apply.pro_address
                # 不写判断会报错
                if pro_apply.sign_date:
                    pro.sign_date = pro_apply
                if pro_apply.start_date:
                    pro.start_date = pro_apply.start_date
                if pro_apply.finish_date:
                    pro.finish_date = pro_apply.finish_date
                # 上传文件才修改原有值，否则不修改
                if pro_apply.ht_scan:
                    pro.ht_scan = pro_apply.ht_scan
                pro.remark = pro_apply.remark
                pro.save()

                # 新建 工程项目成员 信息，且设为 负责人
                pro_member = ProjectMember()
                pro_member.is_pro_person = 1  # 设为 负责人
                pro_member.project_id = pro.id
                pro_member.project_name = pro_apply.project_name
                pro_member.person_id = pro_apply.pro_person_id
                pro_member.person_name = pro_apply.pro_person
                pro_member.department_id = pro_apply.department_id
                pro_member.department = pro_apply.department
                pro_member.save()

                pro_apply.status = '审核通过'
                pro_apply.save()

                return HttpResponse('{"status":"success","msg":"同意工程添加申请操作成功"}', content_type='application/json')

            elif pro_apply.type == '修改信息':
                # 修改了 工程负责人
                if pro_apply.pro_person_id != pro.pro_person_id:
                    # 删除原有的 工程负责人 信息
                    old_pro_member = ProjectMember.objects.get(is_pro_person=1)
                    old_pro_member.delete()
                    # 新建 工程项目成员 信息，且设为 负责人
                    pro_member = ProjectMember()
                    pro_member.is_pro_person = 1  # 设为 负责人
                    pro_member.project_id = pro.id
                    pro_member.project_name = pro_apply.project_name
                    pro_member.person_id = pro_apply.pro_person_id
                    pro_member.person_name = pro_apply.pro_person
                    pro_member.department_id = pro_apply.department_id
                    pro_member.department = pro_apply.department
                    pro_member.save()

                # 将 工程申请 中的内容写进 工程 信息
                pro.pro_name = pro_apply.project_name

                pro.pro_type_id = pro_apply.pro_type_id
                pro.pro_type_name = pro_apply.pro_type
                pro.pro_stage_id = pro_apply.pro_stage_id
                pro.pro_stage_name = pro_apply.pro_stage
                pro.department_id = pro_apply.department_id
                pro.department = pro_apply.department
                pro.pro_person_id = pro_apply.pro_person_id
                pro.pro_person = pro_apply.pro_person
                pro.wt_person_id = pro_apply.wt_person_id
                pro.wt_person = pro_apply.wt_person
                pro.ht_person_id = pro_apply.ht_person_id
                pro.ht_person = pro_apply.ht_person

                pro.ht_name = pro_apply.ht_name
                pro.ht_num = pro_apply.ht_num
                pro.ht_money = pro_apply.ht_money
                pro.js_money = pro_apply.js_money
                pro.wt_dw = pro_apply.wt_dw
                pro.mobile = pro_apply.mobile
                pro.pro_address = pro_apply.pro_address
                # 不写判断会报错
                if pro_apply.sign_date:
                    pro.sign_date = pro_apply
                if pro_apply.start_date:
                    pro.start_date = pro_apply.start_date
                if pro_apply.finish_date:
                    pro.finish_date = pro_apply.finish_date
                # 上传文件才修改原有值，否则不修改
                if pro_apply.ht_scan:
                    pro.ht_scan = pro_apply.ht_scan
                pro.remark = pro_apply.remark
                pro.save()

                pro_apply.status = '审核通过'
                pro_apply.save()

                return HttpResponse('{"status":"success","msg":"同意工程修改申请操作成功"}', content_type='application/json')

            elif pro_apply.type == '删除工程':
                pro.is_active = 0  # 工程状态设置为无效，保留在数据库
                pro.save()

                pro_apply.status = '审核通过'  # 变更记录 判断的依据
                pro_apply.save()

                return HttpResponse('{"status":"success","msg":"同意工程删除申请操作成功"}', content_type='application/json')

        return HttpResponse('{"status":"success","msg":"同意工程申请操作成功"}', content_type='application/json')


# 拒绝申请 Ajax
class RefuseProView(View):
    def post(self, request):

        pro_apply_id = request.POST.get('pro_apply_id', '')

        pro_apply = ProjectApply.objects.get(id=int(pro_apply_id))
        pro = pro_apply.project

        # 部门负责 或 公司负责 ，拒绝都生效
        if pro_apply.type == '添加工程':
            # 添加的 工程 审核不通过，直接删除
            pro.delete()
            pro_apply.status = '审核未通过'
            pro_apply.save()
            return HttpResponse('{"status":"success","msg":"拒绝工程添加申请操作成功"}', content_type='application/json')

        elif pro_apply.type == '修改信息':
            # 不对 工程 信息作出修改
            pro_apply.status = '审核未通过'
            pro_apply.save()
            return HttpResponse('{"status":"success","msg":"拒绝工程修改申请操作成功"}', content_type='application/json')

        elif pro_apply.type == '删除工程':
            # 不对 工程 信息作出修改
            pro_apply.status = '审核未通过'
            pro_apply.save()
            return HttpResponse('{"status":"success","msg":"拒绝工程删除申请操作成功"}', content_type='application/json')

        return HttpResponse('{"status":"success","msg":"拒绝工程申请操作成功"}', content_type='application/json')


# 变更信息 GET
class ChangeView(View):
    def get(self, request):
        # 根据权限查看 变更记录信息，同 工程浏览
        if request.user.permission == '检测员':
            # 工程负责人 为 自己 ， 工程申请 中状态为 审核通过 的信息
            pro_applys = ProjectApply.objects.filter(Q(pro_person_id=request.user.id) | Q(status='审核通过')).order_by(
                '-add_time')
        elif request.user.permission == '部门负责':
            pro_applys = ProjectApply.objects.filter(
                Q(department_id=request.user.department_id) | Q(status='审核通过')).order_by('-add_time')
        elif request.user.permission == '公司负责':
            pro_applys = ProjectApply.objects.filter(status='审核通过').order_by('-add_time')
        else:
            pro_applys = []

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            pro_applys = pro_applys.filter(Q(pro_type__icontains=search_keywords) |
                                           Q(pro_stage__icontains=search_keywords) |
                                           Q(id__icontains=search_keywords) |
                                           Q(type__icontains=search_keywords) |
                                           Q(status__icontains=search_keywords) |
                                           Q(project_name__icontains=search_keywords) |
                                           Q(person_name__icontains=search_keywords) |
                                           Q(pro_person__icontains=search_keywords) |
                                           Q(department__icontains=search_keywords) |
                                           Q(wt_person__icontains=search_keywords) |
                                           Q(ht_person__icontains=search_keywords) |
                                           Q(ht_name__icontains=search_keywords) |
                                           Q(ht_num__icontains=search_keywords) |
                                           Q(ht_money__icontains=search_keywords) |
                                           Q(js_money__icontains=search_keywords) |
                                           Q(wt_dw__icontains=search_keywords) |
                                           Q(mobile__icontains=search_keywords) |
                                           Q(pro_address__icontains=search_keywords) |
                                           Q(remark__icontains=search_keywords))

        # 排序
        if category == 'pro_apply_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('id')
        elif category == 'pro_apply_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-id')
        elif category == 'pro_type_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_type_id')
        elif category == 'pro_type_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_type_id')
        elif category == 'pro_stage_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_stage_id')
        elif category == 'pro_stage_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_stage_id')
        elif category == 'department_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('department_id')
        elif category == 'department_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-department_id')
        elif category == 'pro_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('pro_person_id')
        elif category == 'pro_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-pro_person_id')
        elif category == 'wt_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('wt_person_id')
        elif category == 'wt_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-wt_person_id')
        elif category == 'ht_person_id' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_person_id')
        elif category == 'ht_person_id' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_person_id')
        elif category == 'ht_num' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_num')
        elif category == 'ht_num' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_num')
        elif category == 'ht_money' and mode == 'positive':
            pro_applys = pro_applys.order_by('ht_money')
        elif category == 'ht_money' and mode == 'negative':
            pro_applys = pro_applys.order_by('-ht_money')
        elif category == 'js_money' and mode == 'positive':
            pro_applys = pro_applys.order_by('js_money')
        elif category == 'js_money' and mode == 'negative':
            pro_applys = pro_applys.order_by('-js_money')
        elif category == 'mobile' and mode == 'positive':
            pro_applys = pro_applys.order_by('mobile')
        elif category == 'mobile' and mode == 'negative':
            pro_applys = pro_applys.order_by('-mobile')
        elif category == 'sign_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('sign_date')
        elif category == 'sign_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-sign_date')
        elif category == 'start_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('start_date')
        elif category == 'start_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-start_date')
        elif category == 'finish_date' and mode == 'positive':
            pro_applys = pro_applys.order_by('finish_date')
        elif category == 'finish_date' and mode == 'negative':
            pro_applys = pro_applys.order_by('-finish_date')
        elif category == 'add_time' and mode == 'positive':
            pro_applys = pro_applys.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            pro_applys = pro_applys.order_by('-add_time')

        return render(request, 'project/change.html', {
            'pro_applys': pro_applys
        })


# 考勤记录 GET
class AttendanceView(View):
    def get(self, request):

        # 检测员 获取 当前用户 的考勤记录
        if request.user.permission == '检测员':
            atts = ProjectAttendance.objects.filter(person_id=request.user.id).order_by('-add_time')
            # 部门负责 获取部门所有考勤
        elif request.user.permission == '部门负责':
            atts = ProjectAttendance.objects.filter(department_id=request.user.department_id).order_by('-add_time')
        elif request.user.permission == '公司负责':
            # 公司负责 获取全公司考勤
            atts = ProjectAttendance.objects.all().order_by('-add_time')
        else:
            atts = []

        return render(request, 'project/attendance.html', {
            'atts': atts
        })


# 个人考勤记录 GET
class StaffAttendanceView(View):
    def get(self, request, staff_id):

        # 获取 指定用户 的考勤记录
        atts = ProjectAttendance.objects.filter(person_id=staff_id).order_by('-add_time')

        return render(request, 'project/attendance.html', {
            'atts': atts,
            'individual': 1
        })


# 添加考勤 GET POST
class AddAttendanceView(View):
    def get(self, request):
        # 当前用户为 项目成员 的工程
        pro_members = ProjectMember.objects.filter(person_id=request.user.id)

        pros = []
        for pro_member in pro_members:
            if pro_member.project.is_active == 1:
                pros.append(pro_member.project)

        return render(request, 'project/add_attendance.html', {
            'pros': pros
        })

    def post(self, request):
        pro_id = request.POST.get('pro_id', '')
        time = request.POST.get('time', '')
        location = request.POST.get('location', '')
        remark = request.POST.get('remark', '')

        pro_att = ProjectAttendance()
        pro_att.project_id = pro_id
        pro_att.project_name = Project.objects.get(id=pro_id).pro_name
        pro_att.person_id = request.user.id
        pro_att.person_name = request.user.name
        pro_att.department_id = Project.objects.get(id=pro_id).department_id
        pro_att.department = Project.objects.get(id=pro_id).department
        pro_att.time = time
        pro_att.location = location
        pro_att.remark = remark
        pro_att.save()

        # 获取 当前用户 的考勤记录
        atts = ProjectAttendance.objects.filter(person_id=request.user.id)

        return render(request, 'project/attendance.html', {
            'atts': atts
        })


# 添加工程项目成员 Ajax
class AddMemberView(View):
    def post(self, request):
        person_id = request.POST.get('person_id', '')
        project_id = request.POST.get('project_id', '')

        if ProjectMember.objects.filter(project_id=project_id, person_id=person_id):
            return HttpResponse('{"status":"success","msg":"该工程项目成员已存在，请勿重复添加！"}', content_type='application/json')
        else:
            pro_member = ProjectMember()
            pro_member.is_pro_person = 0 # 非 工程负责人
            pro_member.project_id = project_id
            pro_member.project_name = Project.objects.get(id=project_id).pro_name
            pro_member.person_id = person_id
            pro_member.person_name = UserProfile.objects.get(id=person_id)
            pro_member.department_id = Project.objects.get(id=project_id).department_id
            pro_member.department = Project.objects.get(id=project_id).department
            pro_member.save()

            return HttpResponse('{"status":"success","msg":"添加工程项目成员操作成功"}', content_type='application/json')


# 删除工程项目成员 Ajax
class DeleteMemberView(View):
    def post(self, request):
        pro_member_id = request.POST.get('pro_member_id', '')

        pro_member = ProjectMember.objects.get(id=pro_member_id)
        pro_member.delete()

        return HttpResponse('{"status":"success","msg":"删除工程项目成员操作成功"}', content_type='application/json')


# 添加工程设备 Ajax
class AddEquView(View):
    def post(self, request):
        equ_id = request.POST.get('equ_id', '')
        project_id = request.POST.get('project_id', '')

        if ProjectEquipment.objects.filter(project_id=project_id, equipment_id=equ_id):
            return HttpResponse('{"status":"success","msg":"该工程设备已存在，请勿重复添加！"}', content_type='application/json')
        else:
            pro_equ = ProjectEquipment()
            pro_equ.project_id = project_id
            pro_equ.project_name = Project.objects.get(id=project_id).pro_name
            pro_equ.equipment_id = equ_id
            pro_equ.equipment_name = Equipment.objects.get(id=equ_id)
            pro_equ.save()

            return HttpResponse('{"status":"success","msg":"添加工程设备操作成功"}', content_type='application/json')


# 删除工程设备 Ajax
class DeleteEquView(View):
    def post(self, request):
        pro_equ_id = request.POST.get('pro_equ_id', '')

        pro_equ = ProjectEquipment.objects.get(id=pro_equ_id)
        pro_equ.delete()

        return HttpResponse('{"status":"success","msg":"删除工程设备操作成功"}', content_type='application/json')
