#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from rbac.models import Menu, Permission
from rbac.forms.menu import MenuModelForm


class SecondMenuAddView(CreateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/add_edit.html"
    form_class = MenuModelForm
    success_url = reverse_lazy('rbac:menu_list')


class SecondMenuEditView(UpdateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Menu
    template_name = "rbac/add_edit.html"
    form_class = MenuModelForm
    success_url = reverse_lazy('rbac:menu_list')


class SecondMenuDelView(DeleteView):
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
