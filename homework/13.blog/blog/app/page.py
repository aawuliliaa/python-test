#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.core.paginator import Paginator, EmptyPage


def my_page(queryset, current_page_num):
    """

    :param queryset:
    :param current_page_num:
    :return:
    """
    # 分页器
    # 3是每页显示几条数据
    paginator = Paginator(queryset, 5)
    current_page_num = int(current_page_num)
    # 这里是分页最多列出5个
    # page_range是用于前面展示页码的
    if paginator.num_pages > 5:

        if current_page_num - 2 < 1:
            page_range = range(1, 6)
        elif current_page_num + 2 > paginator.num_pages:
            page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 2, current_page_num + 3)
    else:
        page_range = paginator.page_range

    try:
        # 当前页面的数据
        current_page = paginator.page(current_page_num)
    except EmptyPage as e:
        print(e)
        current_page = paginator.page(1)
    return {"page_range": page_range, "current_page": current_page, "current_page_num": current_page_num}
