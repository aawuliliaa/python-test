#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from django import template
from web.password_crypt import decrypt_p
from web.models import Privilege, MyUser
register = template.Library()


@register.filter
def decode_password(password):
    """
    主机登录用户信息解析密码显示
    因为在保存到数据库的时候，密码是加密的，所以显示的时候要解密
    :param password:
    :return:
    """
    return decrypt_p(password)


@register.filter
def identify_privilege(email, privilege):
    """
    判断当前用户是否有相应的权限，用于页面中某些内容的显示
    :param email:
    :param privilege:
    :return:
    """
    if MyUser.objects.filter(email=email).first().is_admin:
        # 如果是管理员，就返回True，意思是有相应的权限
        return True
    pri_list = list(Privilege.objects.filter(role__users__email=email).values("name"))
    # [{'name': 'add'}, {'name': 'del'}, {'name': 'show'}]
    for index, value in enumerate(pri_list):
        if value.get("name") == privilege:
            # 如果配置了权限，就返回True，意思是有相应的权限
            return True
    # 没有权限，返回False
    return False
