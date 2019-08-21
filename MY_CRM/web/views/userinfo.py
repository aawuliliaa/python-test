#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect
from stark.service.v1 import StarkHandler, get_choice_text, StarkModelForm, StarkForm, Option
from web import models
from web.utils.md5 import gen_md5


class UserInfoAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoChangeModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class ResetPasswordForm(StarkForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoHandler(StarkHandler):

    def display_reset_pwd(self, obj=None, is_header=None):
        if is_header:
            return '重置密码'
        reset_url = self.reverse_commons_url(self.get_url_name('reset_pwd'), pk=obj.pk)
        return mark_safe("<a href='%s'>重置密码</a>" % reset_url)

    list_display = ['nickname', get_choice_text('性别', 'gender'), 'phone', 'email', 'depart', display_reset_pwd]

    search_list = ['nickname__contains', 'name__contains']

    search_group = [
        Option(field='gender'),
        Option(field='depart'),
    ]

    def get_model_form_class(self, is_add=False):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = models.UserInfo.objects.filter(id=pk).first()
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'stark/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def extra_urls(self):
        patterns = [
            url(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                name=self.get_url_name('reset_pwd')),
        ]
        return patterns
