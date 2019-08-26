#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import re_path
from django.shortcuts import render
from django.shortcuts import redirect
from problem.models import FollowUpRecord, Problem
from stark.service.StarkHandler import StarkHandler
from stark.service.StarkModelForm import StarkModelForm
from sign.models import UserInfo


class FollowUpRecordModelForm(StarkModelForm):
    """
    设置字段
    """

    class Meta:
        model = FollowUpRecord
        fields = ["detail"]


class FollowUpRecordHandler(StarkHandler):
    model_form_class = FollowUpRecordModelForm
    list_template = "problem/follow_up_record.html"

    def get_queryset(self, request, *args, **kwargs):
        problem_id = kwargs.get('problem_id')
        return self.model_class.objects.filter(problem_id=problem_id)

    def list_view(self, request, *args, **kwargs):
        problem_id = kwargs.get("problem_id")
        finish = False
        status = Problem.objects.filter(id=problem_id).first().status
        if status == 3:
            finish = True
        if request.method == "POST":

            Problem.objects.filter(id=problem_id).update(status="3")
            finish = True
        data_list = self.get_queryset(request, *args, **kwargs)
        add_btn = self.get_add_btn(request, *args, **kwargs)
        return render(request, self.list_template, {
            "data_list": data_list,
            'add_btn': add_btn,
            "finish": finish
                                                    })

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
            return render(request, self.add_template or "stark/add_edit.html", {"form": form})

        form = model_form_class(data=request.POST)

        if form.is_valid():
            res = form.save()
            email = request.session["current_user"]["email"]
            # 这里是为了设置问题提出人
            user_id = UserInfo.objects.filter(email=email).first().id
            problem_id = kwargs["problem_id"]
            Problem.objects.filter(id=problem_id).update(status="2")
            FollowUpRecord.objects.filter(id=res.id).update(create_person_id=user_id, problem_id=kwargs["problem_id"])
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, self.add_template or "stark/add_edit.html", {"form": form})

    def get_urls(self):
        patterns = [
            re_path(r'^list/(?P<problem_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<problem_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(?P<problem_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
            re_path(r'^del/(?P<problem_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.del_view), name=self.get_del_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns
