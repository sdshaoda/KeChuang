# coding:utf-8
from django import forms

from .models import Project


class AddProForm(forms.ModelForm):
    pro_person = forms.CharField(required=True)
    ht_scan = forms.CharField(required=True)

    class Meta:
        model = Project
        fields = ['pro_name']
        # fields = ['pro_name', 'ht_name', 'ht_num', 'ht_money', 'wt_dw', 'wt_person', 'mobile',
        #           'pro_address', 'represent_person', 'sign_date', 'start_date', 'finish_date', 'pro_type', 'equipment']
