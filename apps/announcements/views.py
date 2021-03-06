# coding:utf-8
from datetime import date

from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from KeChuang.settings import EMAIL_FROM
from equipments.models import Equipment
from users.models import UserProfile, Department
from .models import Announcement, Document


# 公告列表 GET
class ListView(View):
    def get(self, request):
        # 公告是所有员工都能够浏览的
        anns = Announcement.objects.all()

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            anns = anns.filter(Q(id__icontains=search_keywords) |
                               Q(person_name__icontains=search_keywords) |
                               Q(department_name__icontains=search_keywords) |
                               Q(title__icontains=search_keywords) |
                               Q(content__icontains=search_keywords) |
                               Q(remark__icontains=search_keywords))

        # 排序
        if category == 'ann_id' and mode == 'positive':
            anns = anns.order_by('id')
        elif category == 'ann_id' and mode == 'negative':
            anns = anns.order_by('-id')
        elif category == 'person_name' and mode == 'positive':
            anns = anns.order_by('person_name')
        elif category == 'person_name' and mode == 'negative':
            anns = anns.order_by('-person_name')
        elif category == 'department_name' and mode == 'positive':
            anns = anns.order_by('department_name')
        elif category == 'department_name' and mode == 'negative':
            anns = anns.order_by('-department_name')
        elif category == 'title' and mode == 'positive':
            anns = anns.order_by('title')
        elif category == 'title' and mode == 'negative':
            anns = anns.order_by('-title')
        elif category == 'content' and mode == 'positive':
            anns = anns.order_by('content')
        elif category == 'content' and mode == 'negative':
            anns = anns.order_by('-content')
        elif category == 'remark' and mode == 'positive':
            anns = anns.order_by('remark')
        elif category == 'remark' and mode == 'negative':
            anns = anns.order_by('-remark')
        elif category == 'add_time' and mode == 'positive':
            anns = anns.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            anns = anns.order_by('-add_time')

        # 因为登录后进入此页，所以设备归还日期在此处验证
        equs = Equipment.objects.filter(equ_staff_id=request.user.id)
        for equ in equs:
            delta = equ.revert_date - date.today()
            # 归还日期在一周内
            if delta.days < 7:
                msg = '您有设备已快过期，请尽快归还！'
                # 若用户填写了邮箱地址，发邮件
                if request.user.email:
                    email_title = '距设备归还时间还有{0}天'.format(delta.days)
                    email_body = '您已领用的设备：{0}已接近归还日期，距归还日期还有{1}天，请您尽快归还。' \
                                 '另外，我们不排除您还有其他设备已接近归还时间，请仔细核对您所领用的设备。' \
                                 '请在归还日期内归还！'.format(equ.equ_name, delta.days)

                    # 发送状态，成功为 1，失败为 0
                    send_status = send_mail(email_title, email_body, EMAIL_FROM, [request.user.email])
                    if send_status:
                        msg += '已发送邮件至您的邮箱'
                # 弹窗
                return render(request, 'announcement/list.html', {
                    'anns': anns,
                    'msg': msg
                })

        return render(request, 'announcement/list.html', {
            'anns': anns
        })


# 删除公告 Ajax
class DeleteAnnView(View):
    def post(self, request):
        ann_id = request.POST.get('ann_id', '')
        ann = Announcement.objects.get(id=int(ann_id))
        ann.delete()

        if Announcement.objects.filter(id=int(ann_id)):
            return HttpResponse('{"status":"fail","msg":"删除公告失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除公告成功"}', content_type='application/json')


# 发布公告 GET POST
class PublishView(View):
    def get(self, request):
        # 只有 公司负责 和 系统管理员 能够发布公告
        departments = Department.objects.all()

        return render(request, 'announcement/publish.html', {
            'departments': departments
        })

    def post(self, request):
        title = request.POST.get('title', '')
        person_id = request.POST.get('person_id', '')
        department_id = request.POST.get('department_id', '')
        content = request.POST.get('content', '')
        remark = request.POST.get('remark', '')

        announcement = Announcement()
        announcement.title = title
        announcement.person_id = person_id
        announcement.person_name = UserProfile.objects.get(id=int(person_id))
        announcement.department_id = department_id
        announcement.department_name = Department.objects.get(id=int(department_id))
        announcement.content = content
        announcement.remark = remark
        announcement.save()

        anns = Announcement.objects.all()

        return render(request, 'announcement/list.html', {
            'anns': anns
        })


# 公告详情 GET
class DetailView(View):
    def get(self, request, ann_id):
        ann = Announcement.objects.get(id=int(ann_id))
        return render(request, 'announcement/detail.html', {
            'ann': ann
        })


# 公文列表 GET
class DocListView(View):
    def get(self, request):
        docs = Document.objects.all().order_by('-add_time')

        # 公司负责 和 系统管理员 能够浏览 “全公司” 和 各部门 的公文
        # 检测员 和 部门负责 只能浏览 “全公司” 和 本部门 的公文
        if request.user.permission == '检测员' or request.user.permission == '部门负责':
            docs = docs.filter(Q(department=request.user.department) | Q(department_name='全公司'))

        search_keywords = request.GET.get('keywords', '')
        category = request.GET.get('category', '')
        mode = request.GET.get('mode', '')

        # 搜索
        if search_keywords:
            docs = docs.filter(Q(id__icontains=search_keywords) |
                               Q(person_name__icontains=search_keywords) |
                               Q(department_name__icontains=search_keywords) |
                               Q(name__icontains=search_keywords) |
                               Q(document__icontains=search_keywords) |
                               Q(remark__icontains=search_keywords))

        # 排序
        if category == 'doc_id' and mode == 'positive':
            docs = docs.order_by('id')
        elif category == 'doc_id' and mode == 'negative':
            docs = docs.order_by('-id')
        elif category == 'person_name' and mode == 'positive':
            docs = docs.order_by('person_name')
        elif category == 'person_name' and mode == 'negative':
            docs = docs.order_by('-person_name')
        elif category == 'department_name' and mode == 'positive':
            docs = docs.order_by('department_name')
        elif category == 'department_name' and mode == 'negative':
            docs = docs.order_by('-department_name')
        elif category == 'name' and mode == 'positive':
            docs = docs.order_by('name')
        elif category == 'name' and mode == 'negative':
            docs = docs.order_by('-name')
        elif category == 'document' and mode == 'positive':
            docs = docs.order_by('document')
        elif category == 'document' and mode == 'negative':
            docs = docs.order_by('-document')
        elif category == 'remark' and mode == 'positive':
            docs = docs.order_by('remark')
        elif category == 'remark' and mode == 'negative':
            docs = docs.order_by('-remark')
        elif category == 'add_time' and mode == 'positive':
            docs = docs.order_by('add_time')
        elif category == 'add_time' and mode == 'negative':
            docs = docs.order_by('-add_time')

        return render(request, 'announcement/document.html', {
            'docs': docs
        })


# 公文上传
class DocUploadView(View):
    def get(self, request):

        departments = Department.objects.all()

        # 公司负责 和 系统管理员 可上传公文至 “全公司” 和 各部门
        # 部门负责 只能上传公文至 本部门
        if request.user.permission == '部门负责':
            departments = departments.filter(id=request.user.department_id)

        return render(request, 'announcement/upload.html', {
            'departments': departments
        })

    def post(self, request):

        person_id = request.POST.get('person_id', '')
        department_id = request.POST.get('department_id', '')
        name = request.POST.get('name', '')
        document = request.FILES.get('document', '')
        remark = request.POST.get('remark', '')

        doc = Document()
        doc.person_id = person_id
        doc.person_name = UserProfile.objects.get(id=person_id)
        doc.department_id = department_id
        doc.department_name = Department.objects.get(id=department_id)
        doc.name = name
        doc.document = document
        doc.remark = remark
        doc.save()

        if Document.objects.filter(id=doc.id):
            return HttpResponse('{"status":"success","msg":"上传公文成功"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"上传公文成功"}', content_type='application/json')


# 删除公文 Ajax
class DeleteDocView(View):
    def post(self, request):
        doc_id = request.POST.get('doc_id', '')
        doc = Document.objects.get(id=doc_id)
        doc.delete()

        if Announcement.objects.filter(id=doc_id):
            return HttpResponse('{"status":"fail","msg":"删除公文失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除公文成功"}', content_type='application/json')
