#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rbac.models import Menu
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


class MenuAddView(CreateView):
    """
    添加菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Menu
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
