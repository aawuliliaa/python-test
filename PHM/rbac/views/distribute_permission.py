#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.shortcuts import render, reverse, HttpResponse
from django.utils.module_loading import import_string
from django.conf import settings
from rbac.models import Role, Menu, Permission


def distribute_permission(request):
    user_id = request.GET.get("uid")
    role_id = request.GET.get("rid")
    user_module_class = import_string(settings.RBAC_USER_MODLE_CLASS)

    user_obj = user_module_class.objects.filter(id=user_id).first()
    # 用户可能随意输入uid,rid，所以这里做个判断
    if not user_obj:
        user_id = None
    role_obj = Role.objects.filter(id=role_id).first()
    if not role_obj:
        role_id = None
    # 配置用户拥有的角色信息
    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三张表（关系表）
        if not user_obj:
            return HttpResponse('请选择用户，然后再分配角色！')
        user_obj.roles.set(role_id_list)
    # 配置角色拥有的权限
    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_obj:
            return HttpResponse('请选择角色，然后再分配权限！')
        role_obj.permissions.set(permission_id_list)

    # 如果用户输入的uid存在，就获取该用户当前的角色
    if user_id:
        user_has_roles = user_obj.roles.all()
    else:
        user_has_roles = []
    # 把这样方便前端做判断
    # {% if node.id in user_has_permissions_list %}checked{% endif %}
    # 设置所选的用户拥有的角色信息，并在前端checked复选框选中
    user_has_roles_list = [item.id for item in user_has_roles]

    # 查询选中的用户或角色拥有的权限信息
    if role_obj:
        # 选中了角色
        user_has_permissions = role_obj.permissions.all()
        user_has_permissions_list = [item.id for item in user_has_permissions]
    elif user_obj:
        # 选中了用户
        user_has_permissions = user_obj.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_list = [item["permissions"] for item in user_has_permissions]
    else:
        user_has_permissions_list = []
    # user_has_permissions_list = [item.id for item in user_has_permissions]

    all_user_list = user_module_class.objects.all()
    all_role_list = Role.objects.all()
    # 所有的菜单（一级菜单）
    # 下面的一大堆代码，都是为了----为menu添加second_menu，为second_menu添加权限
    # 转换为字典，是为了方便获取数据
    # 同时还有一点需要注意，由于字典是可变类型，后面改了，all_menu_list中的内容也跟着变了
    all_menu_list = Menu.objects.values('id', 'title')
    """
    [
        {id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,'children':[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1 },]},
        {id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2 },{id:5,title:x1, menu_id:2 },]},
        {id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3 },]},
    ]
    """
    all_menu_dict = {}
    """
       {
           1:{id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1,children:[] },]},
           2:{id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2,children:[] },{id:5,title:x1, menu_id:2,children:[] },]},
           3:{id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3,children:[] },]},
       }
       """
    # 注意：
    for item in all_menu_list:
        # item修改了，all_menu_list中每个列表项的值也改了
        item['children'] = []
        all_menu_dict[item['id']] = item

    # 所有二级菜单
    all_second_menu_list = Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    """
    [
        {id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        {id:2,title:x1, menu_id:1,children:[] },
        {id:3,title:x1, menu_id:2,children:[] },
        {id:4,title:x1, menu_id:3,children:[] },
        {id:5,title:x1, menu_id:2,children:[] },
    ]
    """
    all_second_menu_dict = {}
    """
        {
            1:{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
            2:{id:2,title:x1, menu_id:1,children:[] },
            3:{id:3,title:x1, menu_id:2,children:[] },
            4:{id:4,title:x1, menu_id:3,children:[] },
            5:{id:5,title:x1, menu_id:2,children:[] },
        }
        """
    for row in all_second_menu_list:
        row['children'] = []
        # item修改了，all_menu_list中每个列表项的值也改了
        all_second_menu_dict[row['id']] = row

        menu_id = row['menu_id']
        #  # item修改了，all_menu_list中每个列表项的值也改了
        # 因为字典是可变类型，使用的内存空间是同一块，所以会联动改变
        all_menu_dict[menu_id]['children'].append(row)

    # 所有三级菜单（不能做菜单的权限）
    all_permission_list = Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    """
    [
        {id:11,title:x2,pid:1},
        {id:12,title:x2,pid:1},
        {id:13,title:x2,pid:2},
        {id:14,title:x2,pid:3},
        {id:15,title:x2,pid:4},
        {id:16,title:x2,pid:5},
    ]
    """
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {
                    'id':11, 
                    title:'账单列表',
                    children:[
                        {'id':12,title:'添加账单'}
                    ]
                },
                {'id':11, title:'客户列表'},
            ]
        },

    ]
    """

    return render(request, "rbac/distribute_permission.html", {
        'user_list': all_user_list,
        'user_id': user_id,
        'role_list': all_role_list,
        'all_menu_list': all_menu_list,
        'role_id': role_id,
        'user_has_roles_list': user_has_roles_list,
        "user_has_permissions_list": user_has_permissions_list,
    })