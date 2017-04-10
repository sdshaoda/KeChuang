# coding:utf-8
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from users.models import UserProfile, Department
from .models import Announcement, Document


# 公告列表 GET
class ListView(View):
    def get(self, request):
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

        return render(request, 'announcement/list.html', {
            'anns': anns
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
        title = request.POST.get('title', '')
        person_id = request.POST.get('person_id', '')
        department_id = request.POST.get('department_id', '')
        content = request.POST.get('content', '')
        remark = request.POST.get('remark', '')

        announcement = Announcement()
        announcement.title = title
        announcement.person_id = person_id
        announcement.person_name = UserProfile.objects.get(id=person_id)
        announcement.department_id = department_id
        announcement.department_name = Department.objects.get(id=department_id)
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
            return HttpResponse('{"status":"fail","msg":"删除公告失败"}', content_type='application/json')
        return HttpResponse('{"status":"success","msg":"删除公告成功"}', content_type='application/json')
