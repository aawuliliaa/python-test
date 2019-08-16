#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from app.models import UserInfo


class UserForm(forms.Form):
    # 用户form表单验证，主要功能在于进行字段的验证
    username = forms.CharField(label="用户名",
                               max_length=32,
                               error_messages={"required": "用户名不能为空"},
                               # 设置为input控件,并为其添加样式
                               widget=widgets.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="密码",
                               min_length=3,
                               max_length=32,
                               error_messages={"required": "密码不能为空",
                                               "min_length": "密码不能少于3位",
                                               "max_length": "密码最长32位"},
                               widget=widgets.TextInput(attrs={"class": "form-control"}))
    re_password = forms.CharField(label="确认密码",
                                  min_length=6,
                                  max_length=32,
                                  error_messages={"required": "密码不能为空",
                                                  "min_length": "密码不能少于6位",
                                                  "max_length": "密码最长32位"},
                                  widget=widgets.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="邮箱",
                             max_length=32,
                             error_messages={"required": "邮箱不能为空",
                                             "invalid": "邮箱格式错误"},
                             widget=widgets.EmailInput(attrs={"class": "form-control"}))
    # telephone = forms.CharField(label="手机号",
    #                             validators=[RegexValidator(r'^[0-9]+$', '手机号必须是数字'),
    #                                         RegexValidator(r'^1[3-9][0-9]{9}$', '手机号格式错误')],
    #                             error_messages={"required": "该字段不能为空"},
    #                             widget=widgets.TextInput(attrs={"class": "form-control"}))

    def clean_username(self):
        val = self.cleaned_data.get("username")
        user = UserInfo.objects.filter(username=val).first()
        if user:
            raise ValidationError("该用户已经注册！")
        else:
            return val

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password and re_password:
            if password == re_password:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data
