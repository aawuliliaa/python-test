#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse


class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class):
        """

        :param model_class: 是models中的数据库表对应的类。 models.UserInfo
        :param handler_class: 处理请求的视图函数所在的类
        :return:
        """
        """
        self._registry = [
            {'model_class':models.Depart,'handler':DepartHandler(models.Depart)},
            {'model_class':models.UserInfo,'handler':UserInfoHandler(models.UserInfo)}
            {'model_class':models.Host,'handler': HostHandler(models.Host) }
        ]
        """
        self._registry.append({'model_class': model_class, 'handler': handler_class(model_class)})

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            patterns.append(url(r'%s/%s/list/$' % (app_label, model_name,), handler.changelist_view))
            patterns.append(url(r'%s/%s/add/$' % (app_label, model_name,), handler.add_view))
            patterns.append(url(r'%s/%s/change/(\d+)/$' % (app_label, model_name,), handler.change_view))
            patterns.append(url(r'%s/%s/del/(\d+)/$' % (app_label, model_name,), handler.change_view))

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
