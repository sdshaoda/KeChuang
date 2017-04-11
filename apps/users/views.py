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
        # login_form 中包含了 验证码 相关信息
        login_form = LoginForm()

        # 如果已登录，跳转到公告浏览页
        if request.user.username:
            anns = Announcement.objects.all().order_by('-add_time')

            return render(request, 'announcement/list.html', {
                'anns': anns
            })

        return render(request, 'login.html', {
            'login_form': login_form
        })

    def post(self, request):

        # 验证登录表单
        login_form = LoginForm(request.POST)
        login_form.is_valid()
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 数据库验证
            user = authenticate(username=username, password=password)
            if user is not None:
                # 登录
                login(request, user)

                anns = Announcement.objects.all().order_by('-add_time')
                # 跳转到公告浏览页
                return render(request, 'announcement/list.html', {
                    'anns': anns
                })
            else:
                return render(request, 'login.html', {
                    'msg': '用户名或密码错误',
                    'login_form': login_form
                })
        else:
            return render(request, 'login.html', {
                'msg': '验证码错误',
                'login_form': login_form
            })


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
        staffs = UserProfile.objects.filter(is_superuser=0)

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            staffs = staffs.filter(Q(name__icontains=search_keywords) |
                                   Q(id__icontains=search_keywords) |
                                   Q(username__icontains=search_keywords) |
                                   Q(department_name__icontains=search_keywords) |
                                   Q(sex__icontains=search_keywords) |
                                   Q(job__icontains=search_keywords) |
                                   Q(permission__icontains=search_keywords) |
                                   Q(number__icontains=search_keywords) |
                                   Q(mobile__icontains=search_keywords) |
                                   Q(email__icontains=search_keywords) |
                                   Q(office_phone__icontains=search_keywords) |
                                   Q(home_phone__icontains=search_keywords) |
                                   Q(home_address__icontains=search_keywords) |
                                   Q(xueli__icontains=search_keywords) |
                                   Q(zhicheng__icontains=search_keywords) |
                                   Q(zige__icontains=search_keywords))

        # 排序
        if category == 'staff_id' and mode == 'positive':
            staffs = staffs.order_by('id')
        elif category == 'staff_id' and mode == 'negative':
            staffs = staffs.order_by('-id')
        elif category == 'number' and mode == 'positive':
            staffs = staffs.order_by('number')
        elif category == 'number' and mode == 'negative':
            staffs = staffs.order_by('-number')
        elif category == 'sex' and mode == 'positive':
            staffs = staffs.order_by('sex')
        elif category == 'sex' and mode == 'negative':
            staffs = staffs.order_by('-sex')
        elif category == 'induction_time' and mode == 'positive':
            staffs = staffs.order_by('induction_time')
        elif category == 'induction_time' and mode == 'negative':
            staffs = staffs.order_by('-induction_time')
        elif category == 'add_time' and mode == 'positive':
            staffs = staffs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            staffs = staffs.order_by('-add_time')

        return render(request, 'user/list.html', {
            'staffs': staffs
        })


# 通讯录 GET
class AddressView(View):
    def get(self, request):

        # 获取所有员工信息，过滤掉超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            staffs = staffs.filter(Q(name__icontains=search_keywords) |
                                   Q(username__icontains=search_keywords) |
                                   Q(id__icontains=search_keywords) |
                                   Q(department_name__icontains=search_keywords) |
                                   Q(sex__icontains=search_keywords) |
                                   Q(job__icontains=search_keywords) |
                                   Q(permission__icontains=search_keywords) |
                                   Q(number__icontains=search_keywords) |
                                   Q(mobile__icontains=search_keywords) |
                                   Q(email__icontains=search_keywords) |
                                   Q(office_phone__icontains=search_keywords) |
                                   Q(home_phone__icontains=search_keywords) |
                                   Q(home_address__icontains=search_keywords) |
                                   Q(xueli__icontains=search_keywords) |
                                   Q(zhicheng__icontains=search_keywords) |
                                   Q(zige__icontains=search_keywords))

        # 排序
        if category == 'staff_id' and mode == 'positive':
            staffs = staffs.order_by('id')
        elif category == 'staff_id' and mode == 'negative':
            staffs = staffs.order_by('-id')
        elif category == 'number' and mode == 'positive':
            staffs = staffs.order_by('number')
        elif category == 'number' and mode == 'negative':
            staffs = staffs.order_by('-number')
        elif category == 'sex' and mode == 'positive':
            staffs = staffs.order_by('sex')
        elif category == 'sex' and mode == 'negative':
            staffs = staffs.order_by('-sex')
        elif category == 'mobile' and mode == 'positive':
            staffs = staffs.order_by('mobile')
        elif category == 'mobile' and mode == 'negative':
            staffs = staffs.order_by('-mobile')
        elif category == 'email' and mode == 'positive':
            staffs = staffs.order_by('email')
        elif category == 'email' and mode == 'negative':
            staffs = staffs.order_by('-email')
        elif category == 'induction_time' and mode == 'positive':
            staffs = staffs.order_by('induction_time')
        elif category == 'induction_time' and mode == 'negative':
            staffs = staffs.order_by('-induction_time')
        elif category == 'add_time' and mode == 'positive':
            staffs = staffs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            staffs = staffs.order_by('-add_time')

        return render(request, 'user/address.html', {
            'staffs': staffs
        })


# 员工信息管理 GET
class StaffView(View):
    def get(self, request):

        # 获取所有员工信息，过滤掉超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            staffs = staffs.filter(Q(name__icontains=search_keywords) |
                                   Q(username__icontains=search_keywords) |
                                   Q(id__icontains=search_keywords) |
                                   Q(department_name__icontains=search_keywords) |
                                   Q(sex__icontains=search_keywords) |
                                   Q(job__icontains=search_keywords) |
                                   Q(permission__icontains=search_keywords) |
                                   Q(number__icontains=search_keywords) |
                                   Q(mobile__icontains=search_keywords) |
                                   Q(email__icontains=search_keywords) |
                                   Q(office_phone__icontains=search_keywords) |
                                   Q(home_phone__icontains=search_keywords) |
                                   Q(home_address__icontains=search_keywords) |
                                   Q(xueli__icontains=search_keywords) |
                                   Q(zhicheng__icontains=search_keywords) |
                                   Q(zige__icontains=search_keywords))

        # 排序
        if category == 'staff_id' and mode == 'positive':
            staffs = staffs.order_by('id')
        elif category == 'staff_id' and mode == 'negative':
            staffs = staffs.order_by('-id')
        elif category == 'number' and mode == 'positive':
            staffs = staffs.order_by('number')
        elif category == 'number' and mode == 'negative':
            staffs = staffs.order_by('-number')
        elif category == 'sex' and mode == 'positive':
            staffs = staffs.order_by('sex')
        elif category == 'sex' and mode == 'negative':
            staffs = staffs.order_by('-sex')
        elif category == 'induction_time' and mode == 'positive':
            staffs = staffs.order_by('induction_time')
        elif category == 'induction_time' and mode == 'negative':
            staffs = staffs.order_by('-induction_time')
        elif category == 'add_time' and mode == 'positive':
            staffs = staffs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            staffs = staffs.order_by('-add_time')

        return render(request, 'user/staff.html', {
            'staffs': staffs
        })


# 添加新员工 GET POST
class AddStaffView(View):
    def get(self, request):

        # 用户信息是和 部门 相关的
        departments = Department.objects.filter(is_department=1)

        return render(request, 'user/add_staff.html', {
            'departments': departments
        })

    def post(self, request):
        register_form = AddStaffForm(request.POST)
        register_form.is_valid()
        if register_form.is_valid():
            # 获取表单信息
            username = request.POST.get('username', '')

            if UserProfile.objects.filter(username=username):
                return render(request, 'user/add_staff.html', {
                    'register_form': register_form,
                    'msg': '登录名已经存在！'
                })

            password = request.POST.get('password', '')
            password_repeat = request.POST.get('password_repeat', '')
            if password != password_repeat:
                return render(request, 'user/add_staff.html', {
                    'register_form': register_form,
                    'msg': '两次输入的密码不一致！'
                })

            name = request.POST.get('name', '')
            sex = request.POST.get('sex', '')
            department_id = request.POST.get('department_id', '')
            job = request.POST.get('job', '')
            induction_time = request.POST.get('induction_time', '')
            number = request.POST.get('number', '')
            permission = request.POST.get('permission', '')

            user_profile = UserProfile()
            user_profile.username = username
            user_profile.password = make_password(password)
            user_profile.name = name
            user_profile.sex = sex
            user_profile.department_id = department_id
            user_profile.department_name = Department.objects.get(id=department_id).name
            user_profile.job = job
            user_profile.induction_time = induction_time
            user_profile.number = number
            user_profile.permission = permission
            user_profile.is_active = True
            user_profile.save()

            # 筛除超级用户
            staffs = UserProfile.objects.filter(is_superuser=0)

            # 返回员工信息页
            return render(request, 'user/staff.html', {
                'staffs': staffs
            })
        else:
            return render(request, 'user/add_staff.html', {
                'msg': '表单信息填写不合法'
            })


# 编辑档案 GET
class EditView(View):
    def get(self, request, staff_id):
        # 获取此用户信息
        staff = UserProfile.objects.get(id=int(staff_id))

        # 用户信息是和 部门 相关的
        departments = Department.objects.filter(is_department=1)

        return render(request, 'user/edit.html', {
            'staff': staff,
            'departments': departments
        })


# 编辑档案 Ajax
class EditStaffView(View):
    def post(self, request):
        # 获取表单信息
        staff_id = request.POST.get('staff_id', '')
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
        if image:
            user.image = image
        if zigezs:
            user.zigezs = zigezs
        if xuelizs:
            user.xuelizs = xuelizs
        if zhichengzs:
            user.zhichengzs = zhichengzs
        user.save()

        # 修改的是自己的档案
        if int(staff_id) == request.user.id:
            return HttpResponse('{"status":"success","msg":"编辑个人档案成功"}', content_type='application/json')

        return HttpResponse('{"status":"success","msg":"修改员工信息成功"}', content_type='application/json')


# 人员权限管理 GET Ajax
class PermView(View):
    def get(self, request):

        # 获取所有员工信息，过滤掉超级用户
        staffs = UserProfile.objects.filter(is_superuser=0)

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            staffs = staffs.filter(Q(name__icontains=search_keywords) |
                                   Q(username__icontains=search_keywords) |
                                   Q(id__icontains=search_keywords) |
                                   Q(department_name__icontains=search_keywords) |
                                   Q(sex__icontains=search_keywords) |
                                   Q(job__icontains=search_keywords) |
                                   Q(permission__icontains=search_keywords) |
                                   Q(number__icontains=search_keywords) |
                                   Q(mobile__icontains=search_keywords) |
                                   Q(email__icontains=search_keywords) |
                                   Q(office_phone__icontains=search_keywords) |
                                   Q(home_phone__icontains=search_keywords) |
                                   Q(home_address__icontains=search_keywords) |
                                   Q(xueli__icontains=search_keywords) |
                                   Q(zhicheng__icontains=search_keywords) |
                                   Q(zige__icontains=search_keywords))

        # 排序
        if category == 'staff_id' and mode == 'positive':
            staffs = staffs.order_by('id')
        elif category == 'staff_id' and mode == 'negative':
            staffs = staffs.order_by('-id')
        elif category == 'department_name' and mode == 'positive':
            staffs = staffs.order_by('department_name')
        elif category == 'department_name' and mode == 'negative':
            staffs = staffs.order_by('-department_name')
        elif category == 'job' and mode == 'positive':
            staffs = staffs.order_by('job')
        elif category == 'job' and mode == 'negative':
            staffs = staffs.order_by('-job')
        elif category == 'permission' and mode == 'positive':
            staffs = staffs.order_by('permission')
        elif category == 'permission' and mode == 'negative':
            staffs = staffs.order_by('-permission')
        elif category == 'add_time' and mode == 'positive':
            staffs = staffs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            staffs = staffs.order_by('-add_time')

        return render(request, 'user/permission.html', {
            'staffs': staffs
        })

    def post(self, request):

        # 获取表单信息
        staff_id = request.POST.get('id', '')
        permission = request.POST.get('permission', '')

        # 重设权限
        user = UserProfile.objects.get(id=staff_id)
        user.permission = permission
        user.save()

        if user.permission == permission:
            return HttpResponse('{"status":"success","msg":"修改权限成功"}', content_type='application/json')
        return HttpResponse('{"status":"fail","msg":"修改权限失败"}', content_type='application/json')


# 删除员工 Ajax
class DeleteStaffView(View):
    def post(self, request):
        # 获取表单信息
        staff_id = request.POST.get('staff_id', '')

        # 删除员工
        staff = UserProfile.objects.get(id=staff_id)
        staff.delete()

        if UserProfile.objects.filter(id=staff_id):
            return HttpResponse('{"status":"fail","msg":"删除员工信息失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除员工信息成功"}', content_type='application/json')


# 重置密码 GET Ajax
class ResetView(View):
    def get(self, request):
        return render(request, 'user/reset.html')

    def post(self, request):
        # 获取表单信息
        user_name = request.POST.get('username', '')
        password = request.POST.get('new_password', '')
        password_repeat = request.POST.get('new_password_repeat', '')

        # 两次密码一致
        if password == password_repeat:
            # 根据用户名和新密码 重设密码
            user = UserProfile.objects.filter(username=user_name)
            if not len(user):
                return HttpResponse('{"status":"fail","msg":"用户不存在"}', content_type='application/json')
            encrypt_password = make_password(password)
            user[0].password = encrypt_password
            user[0].save()

            if user[0].password == encrypt_password:
                return HttpResponse('{"status":"success","msg":"修改密码成功"}', content_type='application/json')
            return HttpResponse('{"status":"fail","msg":"修改密码失败"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"两次密码填写不一致"}', content_type='application/json')


# 更改密码 GET Ajax
class ChangeView(View):
    def get(self, request):
        return render(request, 'user/change.html')

    def post(self, request):
        # 根据用户名和新密码 重设密码
        user_name = request.POST.get('username', '')
        password = request.POST.get('new_password', '')
        password_repeat = request.POST.get('new_password_repeat', '')

        # 两次密码一致
        if password == password_repeat:
            user = UserProfile.objects.get(username=user_name)
            # if user is None:
            #     return HttpResponse('{"status":"fail","msg":"用户不存在"}', content_type='application/json')
            encrypt_password = make_password(password)
            user.password = encrypt_password
            user.save()

            if user.password == encrypt_password:
                return HttpResponse('{"status":"success","msg":"修改密码成功"}', content_type='application/json')
            return HttpResponse('{"status":"fail","msg":"修改密码失败"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"两次密码填写不一致"}', content_type='application/json')


# 全局 404 处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 404 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
