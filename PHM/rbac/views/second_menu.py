#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from rbac.models import Menu, Permission
from rbac.forms.second_menu import SecondMenuModelForm

from rbac.service.urls import memory_reverse


class SecondMenuAddView(CreateView):
    """
    添加二级菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/add_edit.html"

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        这里是因为添加或删除成功后，页面中还总是不显示，我觉得可能是reverse_lazy()捣的鬼，就自己重写该方法了

        :return:
        """
        return memory_reverse(self.request, 'rbac:menu_list')

    def __init__(self):
        super().__init__()
        self.menu_obj = None

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        # 设置初始值
        if self.request.method == "GET":
            return SecondMenuModelForm(initial={'menu': self.menu_obj})
        else:
            # post提交的时候，不要忘记设置data
            return SecondMenuModelForm(data=self.request.POST)

    def get(self, request, *args, **kwargs):
        menu_id = kwargs.get("menu_id")
        menu_obj = Menu.objects.filter(id=int(menu_id)).first()
        #  form = SecondMenuModelForm(initial={'menu': menu_object})
        self.menu_obj = menu_obj
        self.object = None
        return super().get(request, *args, **kwargs)


class SecondMenuEditView(UpdateView):
    """
    编辑二级菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/add_edit.html"
    form_class = SecondMenuModelForm

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        这里是因为添加或删除成功后，页面中还总是不显示，我觉得可能是reverse_lazy()捣的鬼，就自己重写该方法了

        :return:
        """
        return memory_reverse(self.request, 'rbac:menu_list')


class SecondMenuDelView(DeleteView):
    """
    删除二级菜单
    组件确实很方便呀，内部已经对get和POST方法做了处理
    同时已经自动做了form.save
    """
    model = Permission
    template_name = "rbac/del.html"
    form_class = SecondMenuModelForm

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        这里是因为添加或删除成功后，页面中还总是不显示，我觉得可能是reverse_lazy()捣的鬼，就自己重写该方法了

        :return:
        """
        return memory_reverse(self.request, 'rbac:menu_list')

    def get_context_data(self, **kwargs):
        #
        context = {
            "cancel_url": reverse('rbac:menu_list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
