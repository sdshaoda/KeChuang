# _*_ coding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Project
from .forms import AddProForm
from users.models import UserProfile

class ListView(View):
    def get(self, request):
        all_pro = Project.objects.all().order_by('-sign_date')
        return render(request, 'project/list.html', {
            'all_pro': all_pro
        })


class AddProView(View):
    def get(self, request):
        all_staffs = UserProfile.objects.all().order_by('id')
        staffs = []
        for staff in all_staffs:
            if staff.name:
                staffs.append(staff)
        return render(request, 'project/add.html', {
            'staffs': staffs
        })

    def post(self, request):
        add_pro_form = AddProForm(request.POST)
        add_pro_form.is_valid()
        if add_pro_form.is_valid():
            pro_name = request.POST.get('pro_name', '')
            ht_num = request.POST.get('ht_num', '')
            ht_name = request.POST.get('ht_name', '')
            ht_money = request.POST.get('ht_money', '')
            wt_dw = request.POST.get('wt_dw', '')
            wt_person = request.POST.get('wt_person', '')
            mobile = request.POST.get('mobile', '')
            pro_address = request.POST.get('pro_address', '')
            represent_person = request.POST.get('represent_person', '')
            sign_date = request.POST.get('sign_date', '')
            start_date = request.POST.get('start_date', '')
            finish_date = request.POST.get('finish_date', '')
            pro_person_username = request.POST.get('pro_person', '')
            pro_person = UserProfile.objects.get(username=pro_person_username)
            pro_type = request.POST.get('pro_type', '')
            equipment = request.POST.get('equipment', '')
            ht_scan = request.FILES.get('ht_scan', '')

            pro_info = Project()
            pro_info.pro_name = pro_name
            pro_info.ht_num = ht_num
            pro_info.ht_name = ht_name
            pro_info.ht_money = ht_money
            pro_info.wt_dw = wt_dw
            pro_info.wt_person = wt_person
            pro_info.mobile = mobile
            pro_info.pro_address = pro_address
            pro_info.represent_person = represent_person
            pro_info.sign_date = sign_date
            pro_info.start_date = start_date
            pro_info.finish_date = finish_date
            pro_info.pro_person = pro_person
            pro_info.pro_type = pro_type
            pro_info.equipment = equipment
            pro_info.ht_scan = ht_scan
            pro_info.save()
            return render(request, 'project/list.html')
        else:
            return render(request, 'project/add.html')


class VerifyView(View):
    def get(self, request):
        return render(request, 'project/verify.html')


class DetailView(View):
    def get(self, request, pro_id):
        pro = Project.objects.get(id=int(pro_id))
        return render(request, 'project/detail.html', {
            'pro': pro
        })


class EditView(View):
    def get(self, request):
        return render(request, 'project/edit.html')


class DeleteView(View):
    def get(self, request):
        return render(request, 'project/list.html')


class ApplyView(View):
    def get(self, request):
        return render(request, 'project/apply.html')


class AttenView(View):
    def get(self, request):
        return render(request, 'project/local.html')
