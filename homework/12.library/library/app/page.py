#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django.core.paginator import Paginator, EmptyPage


def set_page_session(request):
    # 由于三个列表，是分别设置的分页操作，这里主要是让各自的分页互不影响。
    if request.GET.get("author_page"):
        request.session["author_page"] = request.GET.get("author_page")
    elif request.GET.get("publish_page"):
        request.session["publish_page"] = request.GET.get("publish_page")
    elif request.GET.get("book_page"):
        request.session["book_page"] = request.GET.get("book_page")
    else:
        # 访问/index/时，就列出首页
        request.session["book_page"] = 1
        request.session["author_page"] = 1
        request.session["publish_page"] = 1
        
        
def my_page(queryset, current_page_num):
    # 分页器
    # 3是每页显示几条数据
    paginator = Paginator(queryset, 5)
    current_page_num = int(current_page_num)

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

        current_page = paginator.page(current_page_num)
    except EmptyPage as e:
        current_page = paginator.page(1)
    return {"page_range": page_range, "current_page": current_page, "current_page_num": current_page_num}
