# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

from users.models import UserProfile
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
        return render(request, 'announcement/publish.html')

    def post(self, request):
        announcement = Announcement()

        title = request.POST.get('title', '')
        person_name = request.POST.get('person', '')
        person = UserProfile.objects.get(username=person_name)
        department = request.POST.get('department', '')
        content = request.POST.get('content', '')

        announcement.title = title
        announcement.person = person
        announcement.department = department
        announcement.content = content
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


# 公文下载 未做
class DocUploadView(View):
    def post(self, request):
        doc = Document()
        name = request.POST.get('name', '')
        document = request.FILES.get('document', '')
        doc.name = name
        doc.document = document
        doc.save()
        return HttpResponse('{"status":"success","msg":"删除公告成功"}', content_type='application/json')
