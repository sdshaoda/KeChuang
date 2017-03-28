# coding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from announcements.models import Announcement
from .forms import LoginForm, AddStaffForm
from .models import UserProfile, Department


# 重载登录方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录 GET POST
class LoginView(View):
    def get(self, request):
        # login_form 中包含了验证码相关信息
        login_form = LoginForm()
        # 如果已登录，跳转到公告浏览页
        if request.user.username:
            all_anns = Announcement.objects.all().order_by('-add_time')
            return render(request, 'announcement/list.html', {
                'all_anns': all_anns
            })
        # 跳转到登录页
        return render(request, 'login.html', {
            'login_form': login_form
        })

    def post(self, request):
        # 验证登录表单
        login_form = LoginForm(request.POST)
        login_form.is_valid()
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 数据库验证
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 登录
                login(request, user)
                all_anns = Announcement.objects.all().order_by('-add_time')
                # 公告浏览页
                return render(request, 'announcement/list.html', {
                    'all_anns': all_anns
                })
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})


# 退出登录 GET
class LogoutView(View):
    def get(self, request):
        # 注销
        logout(request)
        # 重定向到登录页
        return HttpResponseRedirect(reverse('login'))


# 人员浏览 GET
class ListView(View):
    def get(self, request):
        # 获取所有员工信息，过滤掉超级用户
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

        return render(request, 'user/list.html', {
            'staffs': staffs
        })


# 编辑档案 GET
class EditView(View):
    def get(self, request, staff_id):
        staff = UserProfile.objects.get(id=int(staff_id))
        departments = Department.objects.all()
        return render(request, 'user/edit.html', {
            'staff': staff,
            'departments': departments
        })


# 编辑档案 Ajax
class EditStaffView(View):
    def post(self, request):
        staff_id = request.POST.get('id', '')

        mobile = request.POST.get('mobile', '')
        email = request.POST.get('email', '')
        office_phone = request.POST.get('office_phone', '')
        home_phone = request.POST.get('home_phone', '')
        home_address = request.POST.get('home_address', '')
        xueli = request.POST.get('xueli', '')
        zhicheng = request.POST.get('zhicheng', '')
        zige = request.POST.get('zige', '')
        image = request.FILES.get('image', '')
        zigezs = request.FILES.get('zigezs', '')
        xuelizs = request.FILES.get('xuelizs', '')
        zhichengzs = request.FILES.get('zhichengzs', '')

        # 更新用户信息
        user = UserProfile.objects.get(id=staff_id)
        user.mobile = mobile
        user.email = email
        user.office_phone = office_phone
        user.home_phone = home_phone
        user.home_address = home_address
        user.xueli = xueli
        user.zhicheng = zhicheng
        user.zige = zige
        user.image = image
        user.zigezs = zigezs
        user.xuelizs = xuelizs
        user.zhichengzs = zhichengzs
        user.save()

        # 修改的是自己的档案
        if staff_id == request.user.id:
            return HttpResponse('{"status":"success","msg":"编辑个人档案成功"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"修改员工信息成功"}', content_type='application/json')


# 通讯录 GET
class AddressView(View):
    def get(self, request):
        # 筛除超级用户
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

        return render(request, 'user/address.html', {
            'all_staffs': staffs
        })


# 人员权限管理 GET Ajax
class PermView(View):
    def get(self, request):
        # 筛除超级用户
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

        return render(request, 'user/permission.html', {
            'all_staffs': staffs
        })

    def post(self, request):
        # 根据用户名和权限值 重设权限
        staff_id = request.POST.get('id', '')
        permission = request.POST.get('permission', '')
        user = UserProfile.objects.get(id=staff_id)
        user.permission = permission
        user.save()
        if user.permission == permission:
            return HttpResponse('{"status":"success","msg":"修改权限成功"}', content_type='application/json')
        return HttpResponse('{"status":"fail","msg":"修改权限失败"}', content_type='application/json')


# 员工信息管理 GET
class StaffView(View):
    def get(self, request):
        # 筛除超级用户
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if not staff.is_superuser:
                staffs.append(staff)

        return render(request, 'user/staff.html', {
            'all_staffs': staffs
        })


# 添加新员工 GET POST Ajax ×
class AddStaffView(View):
    def get(self, request):
        departments = Department.objects.all()
        return render(request, 'user/add_staff.html', {
            'departments': departments
        })

    def post(self, request):
        register_form = AddStaffForm(request.POST)
        register_form.is_valid()
        if register_form.is_valid():
            user_name = request.POST.get('username', '')

            if UserProfile.objects.filter(username=user_name):
                return render(request, 'user/add_staff.html', {'register_form': register_form, 'msg': '登录名已经存在！'})

            pass_word = request.POST.get('password', '')
            pass_word_repeat = request.POST.get('password_repeat', '')
            if pass_word != pass_word_repeat:
                return render(request, 'user/add_staff.html', {'register_form': register_form, 'msg': '两次输入的密码不一致！'})

            name = request.POST.get('name', '')
            department_name = request.POST.get('department', '')
            department = Department.objects.get(name=department_name)
            job = request.POST.get('job', '')
            induction_time = request.POST.get('induction_time', '')
            permission = request.POST.get('permission', '')

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.name = name
            user_profile.department = department
            user_profile.job = job
            user_profile.induction_time = induction_time
            user_profile.permission = permission
            user_profile.is_active = True
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 筛除超级用户
            all_staffs = UserProfile.objects.all().order_by('id')
            staffs = []
            for staff in all_staffs:
                if not staff.is_superuser:
                    staffs.append(staff)

            # 返回员工信息页
            return render(request, 'user/list.html', {
                'staffs': staffs
            })
        else:
            return HttpResponse('{"status":"fail","msg":"添加员工失败"}', content_type='application/json')


# 删除员工 Ajax × 405错误
class DeleteStaffView(View):
    def post(self, request):
        # 根据 id 删除员工
        staff_id = request.POST.get('staff_id', '')
        user = UserProfile.objects.get(id=staff_id)
        user.delete()

        if UserProfile.objects.filter(id=staff_id):
            return HttpResponse('{"status":"fail","msg":"删除员工信息失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除员工信息成功"}', content_type='application/json')


# 重置密码 GET Ajax √
class ResetView(View):
    def get(self, request):
        return render(request, 'user/reset.html')

    def post(self, request):
        # 根据用户名和新密码 重设密码
        user_name = request.POST.get('username', '')
        password = request.POST.get('new_password', '')
        user = UserProfile.objects.filter(username=user_name)
        if not len(user):
            return HttpResponse('{"status":"fail","msg":"用户不存在"}', content_type='application/json')
        encrypt_password = make_password(password)
        user[0].password = encrypt_password
        user[0].save()
        if user[0].password == encrypt_password:
            return HttpResponse('{"status":"success","msg":"修改密码成功"}', content_type='application/json')
        return HttpResponse('{"status":"fail","msg":"修改密码失败"}', content_type='application/json')


# 更改密码 GET Ajax √
class ChangeView(View):
    def get(self, request):
        return render(request, 'user/change.html')

    def post(self, request):
        # 根据用户名和新密码 重设密码
        user_name = request.POST.get('username', '')
        password = request.POST.get('new_password', '')
        user = UserProfile.objects.get(username=user_name)
        # if user is None:
        #     return HttpResponse('{"status":"fail","msg":"用户不存在"}', content_type='application/json')
        encrypt_password = make_password(password)
        user.password = encrypt_password
        user.save()

        if user.password == encrypt_password:
            return HttpResponse('{"status":"success","msg":"修改密码成功"}', content_type='application/json')
        return HttpResponse('{"status":"fail","msg":"修改密码失败"}', content_type='application/json')
