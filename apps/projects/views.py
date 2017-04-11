# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Project, ProjectType, ProjectStage, ProjectChange
from operation.models import ProjectChange, ProjectPerson, ProjectMember, ProjectApply, ProjectEquipment, ProjectAttendance
from .forms import AddProForm
from users.models import UserProfile


# 工程浏览 GET
class ListView(View):
    def get(self, request):

        pros = Project.objects.all().order_by('-add_time')

        return render(request, 'project/list.html', {
            'pros': pros
        })


# 添加工程 GET POST
class AddProView(View):
    def get(self, request):

        # 筛除超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        # 工程类型
        pro_types = ProjectType.objects.all()

        # 项目阶段
        pro_stages = ProjectStage.objects.all()

        return render(request, 'project/add.html', {
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages
        })

    def post(self, request):
        # add_pro_form = AddProForm(request.POST)
        # add_pro_form.is_valid()
        # if add_pro_form.is_valid():

        # 获取表单信息
        pro_name = request.POST.get('pro_name', '')
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

        # 初始化 工程 信息
        project = Project()
        project.pro_name = pro_name
        project.pro_type_id = pro_type_id
        project.pro_stage_id = pro_stage_id
        project.pro_person_id = pro_person_id
        # 不写判断会报错
        if wt_person_id:
            project.wt_person_id = wt_person_id
        else:
            project.wt_person_id = None
        if ht_person_id:
            project.ht_person_id = ht_person_id
        else:
            project.ht_person_id = None
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
        project.ht_scan = ht_scan
        project.remark = remark
        project.save()

        # 初始化 工程负责人 信息
        project_person = ProjectPerson()
        project_person.project = project
        project_person.person_id = pro_person_id
        project_person.save()

        pros = Project.objects.all().order_by('-add_time')

        return render(request, 'project/list.html', {
            'pros': pros
        })
        # else:
        #     return render(request, 'project/add.html')


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

        return render(request, 'project/edit.html', {
            'pro': pro,
            'staffs': staffs,
            'pro_types': pro_types,
            'pro_stages': pro_stages
        })


# 编辑工程 POST
class EditProView(View):
    def post(self, request):

        # 获取表单信息
        pro_id = request.POST.get('pro_id', '')
        pro_name = request.POST.get('pro_name', '')
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

        # 修改 工程 信息
        project = Project.objects.get(id=pro_id)
        project.pro_name = pro_name
        project.pro_type_id = pro_type_id
        project.pro_stage_id = pro_stage_id
        project.pro_person_id = pro_person_id
        # 不写判断会报错
        if wt_person_id:
            project.wt_person_id = wt_person_id
        else:
            project.wt_person_id = None
        if ht_person_id:
            project.ht_person_id = ht_person_id
        else:
            project.ht_person_id = None
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

        # 修改 工程负责人 信息
        project_person = ProjectPerson.objects.get(project_id=pro_id)
        project_person.person_id = pro_person_id
        project_person.save()

        pros = Project.objects.all().order_by('-add_time')

        return render(request, 'project/list.html', {
            'pros': pros
        })


# 删除工程 Ajax
class DeleteView(View):
    def post(self, request):

        pro_id = request.POST.get('pro_id', '')

        pro = Project.objects.get(id=pro_id)
        pro.delete()

        if Project.objects.filter(id=pro_id):
            return HttpResponse('{"status":"success","msg":"删除工程操作失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除工程操作成功"}', content_type='application/json')


# 工程申请 GET
class ApplyView(View):
    def get(self, request):
        return render(request, 'project/apply.html')


# 申请详情 GET
class ApplyDetailView(View):
    def get(self, request):
        return render(request, 'project/apply.html')


# 工程审核 GET
class VerifyView(View):
    def get(self, request):
        return render(request, 'project/verify.html')


# 同意申请 Ajax
class AgreeProView(View):
    def get(self, request):
        return HttpResponse('{"status":"success","msg":"拒绝设备归还申请操作成功"}', content_type='application/json')


# 拒绝申请 Ajax
class RefuseProView(View):
    def get(self, request):
        return HttpResponse('{"status":"success","msg":"拒绝设备归还申请操作成功"}', content_type='application/json')


# 考勤记录 GET
class AttendanceView(View):
    def get(self, request):

        # 获取 当前用户 的考勤记录
        atts = ProjectAttendance.objects.filter(person_id=request.user.id)

        return render(request, 'project/attendance.html',{
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
        # 根据 工程 获取工程信息变更的全部记录
        return render(request, 'project/change.html')
