# _*_ coding:utf-8 _*_
from django import forms
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, max_length=20)


# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['username', 'password']


class AddStaffForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']
