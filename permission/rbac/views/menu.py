#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm
from rbac.service.urls import memory_reverse


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """

    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menu_exists = models.Menu.objects.filter(id=menu_id).exists()
    # 用户可能随便输入一个menu_id
    if not menu_exists:
        menu_id = None
    # 如果用户没有点击一级菜单
    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []
    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []
    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menus': second_menus,
            'menu_id': menu_id,
            'second_menu_id': second_menu_id,
            'permissions': permissions,
        }
    )



def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认值）
    :return:
    """

    menu_object = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param pk: 当前要编辑的二级菜单
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse('二级菜单不存在，请重新选择！')
        form.instance.pid = second_menu_object
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk: 当前要编辑的权限ID
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)
