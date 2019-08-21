#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rbac.models import Role
from rbac.forms.role import RoleModelForm


class RoleView(ListView):
    """
    列出role数据
    """
    template_name = 'rbac/role_list.html'
    model = Role
    context_object_name = "data_list"
    queryset = Role.objects.all()
    ordering = ('-id',)


class RoleAddView(CreateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Role
    template_name = "rbac/add_edit.html"
    form_class = RoleModelForm
    success_url = reverse_lazy('rbac:role_list')


class RoleEditView(UpdateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Role
    template_name = "rbac/add_edit.html"
    form_class = RoleModelForm
    success_url = reverse_lazy('rbac:role_list')


class RoleDelView(DeleteView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Role
    template_name = "rbac/del.html"
    form_class = RoleModelForm
    success_url = reverse_lazy('rbac:role_list')

    def get_context_data(self, **kwargs):
        context = {
            "cancel_url": reverse('rbac:role_list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
