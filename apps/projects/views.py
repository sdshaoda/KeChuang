# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Project, ProjectType, ProjectStage, ProjectChange
from operation.models import ProjectChange, ProjectPerson, ProjectMember, ProjectApply, ProjectEquipment
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
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

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
        project.pro_type_id = pro_type_id               # 外键不可为空
        project.pro_stage_id = pro_stage_id             # 外键不可为空
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
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

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
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

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

        # 上传文件才修改原有值，否则不修改

        return render(request, 'project/apply.html')


# 删除工程 Ajax
class DeleteView(View):
    def get(self, request):
        return render(request, 'project/list.html')


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
        return render(request, 'project/verify.html')


# 拒绝申请 Ajax
class RefuseProView(View):
    def get(self, request):
        return render(request, 'project/verify.html')


# 工程考勤
class AttenView(View):
    def get(self, request):
        # 根据 用户 查看考勤记录
        return render(request, 'project/attendance.html')


# 变更信息
class ChangeView(View):
    def get(self, request):
        # 根据 工程 获取工程信息变更的全部记录
        return render(request, 'project/change.html')
