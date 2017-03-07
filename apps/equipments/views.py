from django.shortcuts import render

from django.views.generic import View


class ListView(View):
    def get(self, request):
        return render(request, 'equipment/list.html')


class UseView(View):
    def get(self, request):
        return render(request, 'equipment/use.html')


class RevertView(View):
    def get(self, request):
        return render(request, 'equipment/revert.html')


class InfoView(View):
    def get(self, request):
        return render(request, 'equipment/info.html')


class EditView(View):
    def get(self, request):
        return render(request, 'equipment/edit.html')


class ApplyView(View):
    def get(self, request):
        return render(request, 'equipment/apply.html')


class VerifyView(View):
    def get(self, request):
        return render(request, 'equipment/verify.html')
