#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from permission import settings


class CheckPermissionMiddleware(MiddlewareMixin):
    """
    定义用户访问权限的中间件
    对用户可访问的菜单进行校验
    """
    def process_request(self, request):
        """
        1. 获取当前用户请求的URL
        2. 如果是白名单中的URL放行
        3. 不在白名单中，获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        4. 如果用户没有登陆，session中是没有该key的，提示用户登录，登录后会把能够访问的菜单信息存入url中
        5. 权限信息匹配，在session中有当前访问的URL，放行，不在，拒绝访问
        中间件返回None,是能够继续运行views.py的
        {}.get(key)，key不存在时，不会报错。
        :param request:
        :return:
        """
        white_list = settings.WHITE_LIST
        current_path = request.path_info  # 访问[INFO] "GET /customer/list/?wewe，request.path_info=/customer/list/
        for white_url_li in white_list:
            # 如果是白名单中的url，就放行
            if re.match(white_url_li, current_path):
                return None
        session_permission_url_list = request.session.get(settings.SESSION_PERMISSION_URL_LIST)
        # 如果用户没有登陆，session中是没有该key的，提示用户登录，登录后会把能够访问的菜单信息存入url中
        if session_permission_url_list is None:
            return HttpResponse("session中还没有url信息，请登录之后再访问！")
        # 循环用户可访问的菜单列表，如果当前路径在可访问的菜单列表中，就放行，否则就返回拒绝访问
        print("---------------------", session_permission_url_list)
        # ['/customer/list/', '/customer/add/', '/payment/list/', '/payment/add/']
        flag = False
        for permission_url in session_permission_url_list:
            if re.match(permission_url, current_path):
                flag = True

        if flag is False:
            return HttpResponse("没有访问该菜单的权限")