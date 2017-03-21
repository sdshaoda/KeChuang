# coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

from users.models import UserProfile, Department
from .models import Announcement, Document


# 公告列表 GET
class ListView(View):
    def get(self, request):
        all_anns = Announcement.objects.all().order_by('-add_time')
        return render(request, 'announcement/list.html', {
            'all_anns': all_anns
        })


# 删除公告 Ajax
class DeleteAnnView(View):
    def post(self, request):
        ann_id = request.POST.get('ann_id', '')
        ann = Announcement.objects.get(id=ann_id)
        ann.delete()
        if Announcement.objects.filter(id=ann_id):
            return HttpResponse('{"status":"fail","msg":"删除公告失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除公告成功"}', content_type='application/json')


# 发布公告 GET POST
class PublishView(View):
    def get(self, request):
        departments = Department.objects.all()
        return render(request, 'announcement/publish.html', {
            'departments': departments
        })

    def post(self, request):
        announcement = Announcement()

        title = request.POST.get('title', '')
        person_name = request.POST.get('person', '')
        person = UserProfile.objects.get(username=person_name)
        department_name = request.POST.get('department', '')
        department = Department.objects.get(name=department_name)
        content = request.POST.get('content', '')
        remark = request.POST.get('remark', '')

        announcement.title = title
        announcement.person = person
        announcement.department = department
        announcement.content = content
        announcement.remark = remark
        announcement.save()

        all_anns = Announcement.objects.all().order_by('-add_time')
        return render(request, 'announcement/list.html', {
            'all_anns': all_anns
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
        return render(request, 'announcement/document.html', {
            'docs': docs
        })


# 公文上传
class DocUploadView(View):
    def get(self, request):
        departments = Department.objects.all()
        return render(request, 'announcement/upload.html', {
            'departments':departments
        })

    def post(self, request):
        doc = Document()

        person_name = request.POST.get('person', '')
        person = UserProfile.objects.get(username=person_name)
        department_name = request.POST.get('department', '')
        department = Department.objects.get(name=department_name)

        name = request.POST.get('name', '')
        document = request.FILES.get('document', '')
        remark = request.POST.get('remark', '')

        doc.person = person
        doc.department = department
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
            return HttpResponse('{"status":"fail","msg":"删除公告失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除公告成功"}', content_type='application/json')
