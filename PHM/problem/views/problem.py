#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from stark.service.StarkHandler import StarkHandler
from stark.service.get_text import *
from stark.service.Option import Option
from problem.models import Problem
from sign.models import UserInfo


class ProblemModelForm(forms.ModelForm):
    """
    设置字段
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Problem
        fields = ["desc", "detail", "status",]
        widgets = {
                    'detail': forms.Textarea(
                        attrs={'class': 'form-control', "data-provide": "markdown"}),

                }


class ProblemHandler(StarkHandler):

    def display_follow_up_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        问题跟进记录
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '跟进记录'
        record_url = reverse('stark:problem_followuprecord_list', kwargs={'problem_id': obj.pk})
        return mark_safe('<a  href="%s">跟进记录</a>' % record_url)

    list_display = [StarkHandler.display_checkbox, "desc", "detail", "create_person", "deal_person",
                    get_datetime_text("问题创建时间", "create_time", time_format='%Y-%m-%d %H:%I:%M'),
                    get_datetime_text("问题开始处理时间", "start_deal_time", time_format='%Y-%m-%d %H:%I:%M'),
                    get_datetime_text("问题完成时间", "stop_deal_time", time_format='%Y-%m-%d %H:%I:%M'),
                    get_choice_text("状态", "status"),
                    display_follow_up_record]
    search_list = ['detail', 'desc', ]
    order_list = ["-id"]
    action_list = [StarkHandler.action_multi_delete]
    search_group = [
        Option('status'),
    ]
    model_form_class = ProblemModelForm

    def add_view(self, request, *args, **kwargs):
        """
        添加页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        model_form_class = self.get_model_form_class(True, request, None, *args, **kwargs)
        if request.method == "GET":
            form = model_form_class()
            form.initial["status"] = "1"
            return render(request, self.add_template or "stark/add_edit.html", {"form": form})

        form = model_form_class(data=request.POST)

        if form.is_valid():
            res = form.save()
            email = request.session["current_user"]["email"]
            # 这里是为了设置问题提出人
            user_id = UserInfo.objects.filter(email=email).first().id
            Problem.objects.filter(id=res.id).update(create_person_id=user_id)
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.add_template or "stark/add_edit.html", {"form": form})