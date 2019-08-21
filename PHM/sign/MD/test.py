#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.shortcuts import HttpResponse,render
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class Test(MiddlewareMixin):
    pass
    """
    定义用户访问权限的中间件
    对用户可访问的菜单进行校验
    """
    # def process_request(self, request):
    #     try:
    #         1/0
    #     except Exception as e:
    #         return render(request, "sign/500.html")
    #     return render(request, "sign/404.html")