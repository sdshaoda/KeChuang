# coding:utf-8
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from operation.models import ProjectApply, ProjectAttendance
from users.models import UserProfile, Department
from .models import Project, ProjectType, ProjectStage


# 工程浏览 GET
class ListView(View):
    def get(self, request):

        # 检测员 浏览自己为项目成员的工程（暂时只做负责人）
        if request.user.permission == '检测员':
            pros = Project.objects.filter(Q(pro_person_id=request.user.id)|Q(is_active=1))
        # 部门负责 浏览负责人为本部门员工（ OR 自己为项目成员）
        elif request.user.permission == '部门负责':
            pros = Project.objects.filter(Q(department_id=request.user.department_id)|Q(is_active=1))
        # 公司负责 浏览所有工程
        elif request.user.permission == '公司负责':
            pros = Project.objects.filter(is_active=1)
        else:
            pros = []

        # 搜索 排序

        return render(request, 'project/list.html', {
            'pros': pros
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
            project.pro_type_id = pro_type_id
            project.pro_type_name = ProjectType.objects.get(id=pro_type_id)
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
            project.pro_type_id = pro_type_id
            project.pro_type = ProjectType.objects.get(id=pro_type_id).name
        if pro_stage_id:
            project.pro_stage_id = pro_stage_id
            project.pro_stage = ProjectStage.objects.get(id=pro_stage_id).name
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
        pro_applys = ProjectApply.objects.filter(person_id=request.user.id)
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

        return render(request, 'project/edit.html', {
            'pro': pro,
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages,
            'departments': departments
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

        # 直接修改 工程 信息，并生成 审核通过 的 工程申请
        if request.user.permission == '公司负责':
            project.pro_name = pro_name
            project.pro_type_id = pro_type_id
            project.pro_type_name = ProjectType.objects.get(id=pro_type_id)
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
            project.pro_type_id = pro_type_id
            project.pro_type = ProjectType.objects.get(id=pro_type_id).name
        if pro_stage_id:
            project.pro_stage_id = pro_stage_id
            project.pro_stage = ProjectStage.objects.get(id=pro_stage_id).name
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
        pro_applys = ProjectApply.objects.filter(person_id=request.user.id)
        # 转到 工程申请
        return render(request, 'project/apply.html', {
            'pro_applys': pro_applys
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

        return render(request, 'project/detail.html', {
            'pro': pro,
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages
        })


# 删除工程 Ajax
class DeleteView(View):
    def post(self, request):
        pro_id = request.POST.get('pro_id', '')

        # 初始化 工程申请
        pro = Project.objects.get(id=pro_id)
        pro.delete()

        if Project.objects.filter(id=pro_id):
            return HttpResponse('{"status":"success","msg":"删除工程操作失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除工程操作成功"}', content_type='application/json')


# 工程申请 GET
class ApplyView(View):
    def get(self, request):
        # 申请人 为当前用户的申请
        pro_applys = ProjectApply.objects.filter(person_id=request.user.id)

        return render(request, 'project/apply.html', {
            'pro_applys': pro_applys
        })


# 申请详情 GET
class ApplyDetailView(View):
    def get(self, request, pro_apply_id):
        pro_apply = ProjectApply.objects.get(id=int(pro_apply_id))

        return render(request, 'project/apply_detail.html', {
            'pro_apply': pro_apply
        })


# 工程审核 GET
class VerifyView(View):
    def get(self, request):

        # 部门负责 只接受本部门的申请，且 审核状态 为 部门主任审核中
        if request.user.permission == '部门负责':
            pro_applys = ProjectApply.objects.filter(Q(department=request.user.department.name) | Q(status='部门主任审核中'))
        # 公司负责 接受所有部门的申请，且 审核状态 为 公司领导审核中
        elif request.user.permission == '公司负责':
            pro_applys = ProjectApply.objects.filter(status='公司领导审核中')
        else:
            pro_applys = []

        return render(request, 'project/verify.html', {
            'pro_applys': pro_applys
        })


# 同意申请 Ajax
class AgreeProView(View):
    def get(self, request):

        pro_apply_id = request.POST.get('pro_apply_id', '')

        pro_apply = ProjectApply.objects.get(id=int(pro_apply_id))
        pro = pro_apply.project

        # 判断 工程申请 的类型
        if pro_apply.type == '添加工程':
            pro.is_active = 1
            # 将 申请 中的内容写进 工程 信息
            pro.save()
        elif pro_apply.type == '修改信息':
            # 将 申请 中的内容写进 工程 信息
            pro.save()
        elif pro_apply.type == '删除工程':
            pro.is_active = 0

        return HttpResponse('{"status":"success","msg":"同意工程申请操作成功"}', content_type='application/json')


# 拒绝申请 Ajax
class RefuseProView(View):
    def get(self, request):

        pro_apply_id = request.POST.get('pro_apply_id', '')

        pro_apply = ProjectApply.objects.get(id=int(pro_apply_id))
        pro = pro_apply.project

        # 判断 工程申请 的类型
        if pro_apply.type == '添加工程':
            # 添加的 工程 不通过审核，直接删除
            pro.delete()
        elif pro_apply.type == '修改信息':
            # 将 申请 中的内容写进 工程 信息
            pro.save()
        elif pro_apply.type == '删除工程':
            # 工程 在数据库中依然存在，能查看其 变更记录
            pro.is_active = 0
            pro.save()

        return HttpResponse('{"status":"success","msg":"拒绝工程申请操作成功"}', content_type='application/json')


# 考勤记录 GET
class AttendanceView(View):
    def get(self, request):
        # 获取 当前用户 的考勤记录
        atts = ProjectAttendance.objects.filter(person_id=request.user.id)

        return render(request, 'project/attendance.html', {
            'atts': atts
        })


# 添加考勤 GET POST
class AddAttendanceView(View):
    def get(self, request):
        # 当前用户为 项目成员 的工程（目前暂时只做负责人的）
        pros = Project.objects.filter(pro_person_id=request.user.id)

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
        pro_att.person_id = request.user.id
        pro_att.time = time
        pro_att.location = location
        pro_att.remark = remark
        pro_att.save()

        # 获取 当前用户 的考勤记录
        atts = ProjectAttendance.objects.filter(person_id=request.user.id)

        return render(request, 'project/attendance.html', {
            'atts': atts
        })


# 变更信息 GET
class ChangeView(View):
    def get(self, request):
        # 根据权限查看 变更记录信息，同 工程浏览
        if request.user.permission == '检测员':
            # 工程负责人 为 自己 ， 工程申请 中状态为 审核通过 的信息
            pro_applys = ProjectApply.objects.filter(Q(pro_person_id=request.user.id) | Q(status='审核通过'))
        elif request.user.permission == '部门负责':
            pro_applys = ProjectApply.objects.filter(Q(department_id=request.user.department_id) | Q(status='审核通过'))
        elif request.user.permission == '公司负责':
            pro_applys = ProjectApply.objects.filter(status='审核通过')
        else:
            pro_applys = []

        return render(request, 'project/change.html', {
            'pro_applys': pro_applys
        })
