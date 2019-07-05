#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django import template
from django.db.models import Count
from app.models import *

register = template.Library()
# 渲染html页面
@register.inclusion_tag("classes.html")
def get_classes_data(username):
    """
    获取数据，渲染到html页面中。返回值是渲染后的html页面
    :param username:
    :return:
    """

    user_obj = UserInfo.objects.filter(username=username).first()
    cate_list = Category.objects.filter(user=user_obj).values("pk").\
        annotate(c=Count("article__title")).values_list("title", "c")
    tag_list = Tag.objects.filter(user=user_obj).values("pk").\
        annotate(c=Count("article__title")).values_list("title", "c")
    # 存的是dateTime类型，按照年-月分类
    date_list = Article.objects.filter(user=user_obj).extra(select={"y_m_date": "date_format(create_time,'%%Y-%%m')"}).\
        values("y_m_date").annotate(c=Count("id")).values_list("y_m_date", "c")
    # 返回的是渲染后的html页面
    return {"username": username, "cate_list": cate_list, "date_list": date_list, "tag_list": tag_list}
