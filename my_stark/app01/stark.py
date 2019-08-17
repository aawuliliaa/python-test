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
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from stark.service.v1 import site, StarkHandler, get_choice_text
from app01 import models


# http://127.0.0.1:8000/stark/app01/depart/list/
class DepartHandler(StarkHandler):
    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]


site.register(models.Depart, DepartHandler)


# http://127.0.0.1:8000/stark/app01/userinfo/list/
class UserInfoHandler(StarkHandler):
    # 定制页面显示的列
    list_display = ['name',
                    get_choice_text('性别', 'gender'),
                    get_choice_text('班级', 'classes'),
                    'age', 'email', 'depart',
                    StarkHandler.display_edit,
                    StarkHandler.display_del]


site.register(models.UserInfo, UserInfoHandler)
