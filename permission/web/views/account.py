#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse, render,redirect
from permission import settings
from rbac import models


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

    # 当前用户所有权限
    # permissions__isnull=False是由于有的角色可能没有分配权限，此时permission处为null
    # 由于角色和权限是多对多关系，所以可能存在重复数据，需要distinct()去重
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__url").distinct()
    print("---------------",permission_queryset)
    # permission_set = models.Permission.objects.filter(role__userinfo__name=user)
    # print("---------------",permission_set)

    # 获取权限中所有的URL
    # permission_list = []
    # for item in permission_queryset:
    #     permission_list.append(item['permissions__url'])
    # query_set不能直接放入session中,转换为列表，存入session中
    permission_list = [item['permissions__url'] for item in permission_queryset]
    # 存入session中
    request.session[settings.SESSION_PERMISSION_URL_LIST] = permission_list
    # 登录成功，跳转到熬客户列表页面
    return redirect('/customer/list/')
