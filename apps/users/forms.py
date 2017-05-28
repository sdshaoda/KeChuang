# coding:utf-8
from django import forms
from .models import UserProfile
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, max_length=20)
    captcha = CaptchaField()


# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['username', 'password']


class AddStaffForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username']
