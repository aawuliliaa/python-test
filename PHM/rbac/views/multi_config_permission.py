#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.urls import reverse
from collections import OrderedDict
from rbac.models import Permission
from rbac.service.auto_discover_url import get_all_url_dict

from rbac.forms.multi_config_permission import MultiAddPermissionForm, MultiEditPermissionForm


def multi_config_permission(request):
    """
    formset--批量添加，修改Permission表中数据
    :param request:
    :return:
    """
    post_type = request.GET.get("type")
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    generate_formset = None
    update_formset = None
    # 1.获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    """
        {
            'rbac:role_list':{'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
            'rbac:role_add':{'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
            ....
        }
        """
    # 2.把自动发现的所有URL的name放到集合中
    route_name_set = set(all_url_dict.keys())

    # 3.获取数据库中的所有URL
    permissions = Permission.objects.all().values("id", "title", "name", "url", "menu_id", "pid_id")
    # permissions = <QuerySet[{},{},{},{}]
    permission_dict = OrderedDict()
    """
        {
            'rbac:role_list': {'id':1,'title':'角色列表',name:'rbac:role_list',url.....},
            'rbac:role_add': {'id':1,'title':'添加角色',name:'rbac:role_add',url.....},
            ...
        }
        """
    permission_name_set = set()
    # 4.设置permission_dict
    for row in permissions:
        permission_dict[row.get("name")] = row
        permission_name_set.add(row.get("name"))
    # 5.循环数据库Permission中的数据，检查URL与代码中配置的是否一致，稍后展示在页面中，提示用户
    for name, value in permission_dict.items():
        if name in all_url_dict:
            if all_url_dict[name]["url"] != permission_dict[name]["url"]:
                value["url"] = "数据库中的url与代码中配置的url不一致！"
    # 6.计算出应该添加的name,set(代码中的url)-set(Permission表中的数据),
    # 初始化应该添加的url信息的formset,即generate_formset
    # get请求的时候才设置初始数据
    if not generate_formset:
        generate_name_list = route_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list]
        )

    # 7.计算需要删除的url信息，set(Permission表中的数据)-set(代码中的url)
    delete_name_list = permission_name_set - route_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 8.计算出需要修改的url信息，set(Permission表中的数据) & set(代码中的url)
    # 两个集合取交集
    if not update_formset:
        update_name_list = route_name_set & permission_name_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list]
        )
    return render(request, 'rbac/multi_config_permission.html', {
        "generate_formset": generate_formset,
        "delete_row_list": delete_row_list,
        "update_formset": update_formset
    })


def multi_permissions_del(request, pk):
    """
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    """
    # url = memory_reverse(request, 'rbac:multi_permissions')
    url = reverse('rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/del.html', {'cancel': url})

    Permission.objects.filter(id=pk).delete()
    return redirect(url)