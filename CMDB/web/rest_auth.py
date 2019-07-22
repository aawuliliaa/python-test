#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import authenticate
from rest_framework import exceptions
from web.models import MyUser


class MyApiAuth(BaseAuthentication):
    # 注意我们这个认证的类必须实现的方法以及返回值
    def authenticate(self, request):
        request_user_email = request.query_params.get("email", None)
        request_user_password = request.query_params.get("password", None)
        print(request.query_params)
        if not request_user_email:
            raise exceptions.AuthenticationFailed({"code": 1001, "error": "缺少email"})
        elif not request_user_password:
            raise exceptions.AuthenticationFailed({"code": 1001, "error": "缺少password"})
        user_obj = authenticate(email=request_user_email, password=request_user_password)
        # user_obj = MyUser.objects.filter(email=request_user_email, password=request_user_password).first()
        if not user_obj:
            raise exceptions.AuthenticationFailed({"code": 1001, "error": "无效的用户信息"})
        return user_obj.name, user_obj