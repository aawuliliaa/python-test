#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from stark.service.StarkHandler import StarkHandler
from django.urls import re_path


class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = "stark"
        self.namespace = "stark"

    def register(self, model_class, handler_class=StarkHandler, prev=None):
        """

        :param model_class: 是models中的数据库表对应的类。
        :param handler_class: 处理请求的视图函数的类
        :param prev: 生成URL的前缀，用于区分URL
        :return:
        """
        """
        self._registry = [
            {'prev':None, 'model_class':models.Depart,'handler': DepartHandler(models.Depart,prev)对象中有一个model_class=models.Depart   },
            {'prev':'private', 'model_class':models.UserInfo,'handler':  StarkHandler(models.UserInfo,prev)对象中有一个model_class=models.UserInfo   }
            {'prev':None, 'model_class':models.Host,'handler':  HostHandler(models.Host,prev)对象中有一个model_class=models.Host   }
        ]
        """
        self._registry.append(
            {"model_class": model_class, "handler": handler_class(self, model_class, prev), "prev": prev}
        )

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item["model_class"]
            handler = item["handler"]
            prev = item["prev"]
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            if prev:
                patterns.append(re_path(r"^%s/%s/%s/" % (app_label, model_name, prev), (handler.get_urls(), None, None)))
            else:
                patterns.append(re_path(r"^%s/%s/" % (app_label, model_name), (handler.get_urls(), None, None)))

        return patterns

    @property
    def urls(self):
        # include('sign.urls', namespace='sign')与下面的内容相同
        # 方式二：
        # include函数主要返回有三个元素的元组。
        # from django.conf.urls import url, include
        # from app01 import urls
        # urlpatterns = [
        #     url(r'^web/', (urls, app_name, namespace)),  # 第一个参数是urls文件对象，通过此对象可以获取urls.patterns获取分发的路由。
        # ]
        #
        # re_path(r'^stark/', site.urls),
        return self.get_urls(), self.app_name, self.namespace


# 实例化，单例模式
site = StarkSite()
