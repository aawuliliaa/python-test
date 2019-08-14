#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse, render,redirect
from permission import settings
from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    # 用户不存在
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session。

    init_permission(request, current_user)
    # 登录成功，跳转到熬客户列表页面
    return redirect('/customer/list/')
