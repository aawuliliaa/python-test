#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from django.conf.urls import url
# from django.shortcuts import HttpResponse
# from stark.service.v1 import site, StarkHandler
# from app01 import models


# class DepartHandler(StarkHandler):
#
#     def extra_urls(self):
#         """
#         额外的增加URL
#         :return:
#         """
#         return [
#             url(r'^detail/(\d+)/$', self.detail_view)
#         ]
#
#     def detail_view(self, request, pk):
#         return HttpResponse('详细页面')


# site.register(models.Depart, DepartHandler)

#
# class UserInfoHandler(StarkHandler):
#
#     def get_urls(self):
#         """
#         修改URL
#         :return:
#         """
#         patterns = [
#             url(r'^list/$', self.changelist_view),
#             url(r'^add/$', self.add_view),
#         ]
#
#         return patterns


# class UserInfoHandler(StarkHandler):
#     # 定制页面显示的列
#     list_display = ['name', 'age', 'email']
#     # pass
#
# site.register(models.UserInfo, UserInfoHandler)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from django.conf.urls import url
# from django.shortcuts import HttpResponse
# from django.urls import reverse
# from django.utils.safestring import mark_safe
# from stark.service.v1 import site, StarkHandler, get_choice_text
# from app01 import models
#
#
# # http://127.0.0.1:8000/stark/app01/depart/list/
# class DepartHandler(StarkHandler):
#     list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]
#
#
# site.register(models.Depart, DepartHandler)
#
#
# # http://127.0.0.1:8000/stark/app01/userinfo/list/
# class UserInfoHandler(StarkHandler):
#     # 定制页面显示的列
#     list_display = ['name',
#                     get_choice_text('性别', 'gender'),
#                     get_choice_text('班级', 'classes'),
#                     'age', 'email', 'depart',
#                     StarkHandler.display_edit,
#                     StarkHandler.display_del]
#
#
# site.register(models.UserInfo, UserInfoHandler)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from stark.service.v1 import site, StarkHandler, get_choice_text, StarkModelForm
from django import forms
from app01 import models

from stark.service.v1 import Option
# http://127.0.0.1:8000/stark/app01/depart/list/
class DepartHandler(StarkHandler):
    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]
    has_add_btn = True


site.register(models.Depart, DepartHandler)


# http://127.0.0.1:8000/stark/app01/userinfo/list/
# 添加或编辑的时候，默认展示所有字段
# 这样可以自定义字段
class UserInfoModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'gender', 'classes', 'age', 'email']
class MyOption(Option):
    def get_db_condition(self, request, *args, **kwargs):
        return {}

class UserInfoHandler(StarkHandler):
    # 定制页面显示的列
    list_display = [
        StarkHandler.display_checkbox,
        'name',
                    get_choice_text('性别', 'gender'),
                    get_choice_text('班级', 'classes'),
                    'age', 'email', 'depart',

                    StarkHandler.display_edit,
                    StarkHandler.display_del]

    per_page_count = 10
    order_list = ["id"]
    # 姓名中含有关键字或邮箱中含有关键字
    search_list = ['name__contains', 'email__contains']
    search_group = [
        Option('gender'),
        MyOption('depart', {'id__gt': 2}),
    ]

    has_add_btn = True
    action_list = [StarkHandler.action_multi_delete, ]
    model_form_class = UserInfoModelForm
    # 预留一个save()钩子函数，这样用户可以在自己的Handler中重写save
    def save(self, form, is_update=False):
        form.instance.depart_id = 1
        form.save()


site.register(models.UserInfo, UserInfoHandler)


# ############# Deploy 表操作 #############
class DeployHandler(StarkHandler):
    list_display = ['title',
                    get_choice_text('状态', 'status'),
                    StarkHandler.display_edit,
                    StarkHandler.display_del]


site.register(models.Deploy, DeployHandler)
