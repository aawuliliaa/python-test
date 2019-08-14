#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import re
from django.template import Library
from django.conf import settings

register = Library()
@register.inclusion_tag("rbac/menu.html")
def menu(request):
    menu_list = request.session.get(settings.SESSION_MENU_KEY)
    for item in menu_list:
        if re.match(item["url"], request.path_info):
            item["class"] = "active"
    #         注意这里的返回值，要是字典，前端直接循环menu_list
    return {
        'menu_list': request.session.get(settings.SESSION_MENU_KEY)
    }