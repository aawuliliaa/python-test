#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rbac.models import Menu, Permission
from rbac.forms.menu import MenuModelForm


class MenuView(ListView):
    """
    列出menu数据
    """
    template_name = 'rbac/menu_list.html'
    model = Menu
    context_object_name = "data_list"
    queryset = Menu.objects.all()
    ordering = ('-id',)

    def get_context_data(self, **kwargs):
        second_menu_list = ""
        permission_list = ""
        # 用户点击一级菜单的a标签的时候，列出对应的二级菜单的信息
        menu_id = self.request.GET.get("mid", "")
        # second_menu_id 即当用户点击二级菜单的时候，展示对应的权限信息
        sid = self.request.GET.get("sid", "")
        if menu_id:
            second_menu_list = Permission.objects.filter(menu_id=int(menu_id))
        if sid:
            # menu_id为空，pid_id不为空的，就是权限---即二级菜单中的按钮
            permission_list = Permission.objects.filter(pid_id=int(sid), menu_id__isnull=True)
        context = {
            "menu_list": self.queryset,
            "second_menu_list": second_menu_list,
            "permission_list": permission_list,
            "mid": menu_id,
            "sid": sid
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class MenuAddView(CreateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/add_edit.html"
    form_class = MenuModelForm
    success_url = reverse_lazy('rbac:menu_list')


class MenuEditView(UpdateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Menu
    template_name = "rbac/add_edit.html"
    form_class = MenuModelForm
    success_url = reverse_lazy('rbac:menu_list')


class MenuDelView(DeleteView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Menu
    template_name = "rbac/del.html"
    form_class = MenuModelForm
    success_url = reverse_lazy('rbac:menu_list')

    def get_context_data(self, **kwargs):
        context = {
            "cancel_url": reverse('rbac:menu_list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
