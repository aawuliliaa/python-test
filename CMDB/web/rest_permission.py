#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from rest_framework.permissions import BasePermission
from CMDB import settings


class MyApiPermission(BasePermission):
    message = "角色编码为API_user的用户才能请求"

    def has_permission(self, request, view):
        """
        自定义权限只有角色编码为API_user的用户才能请求，
        注意我们初始化时候的顺序是认证在权限前面的，所以只要认证通过~
        我们这里就可以通过request.user,拿到我们用户信息
        request.auth就能拿到用户对象
        """
        # 这里反向查询是使用Role表中的related_name='users_role'，如果不使用这个，还可以使用request.auth.role_set.all()
        # print("hhhhhhhhhhhhhhh",request.auth.users_role.all())  # <QuerySet [<Role: API_user>]>
        # 没有权限时，urllib访问报错urllib.error.HTTPError: HTTP Error 403: Forbidden
        role_set = request.auth.users_role.all()
        if request.user and role_set:
            if role_set.first().code == settings.REST_OWN_PERMISSION_USER_ROLE_CODE:
                return True
            else:
                return False
# 测试代码
# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # Author: vita
# from  urllib import request
# import json
# req = request.Request("http://10.0.0.61:8080/api/Role?email=sasa@qq.com&password=123")
# page = request.urlopen(req).read()
# page = page.decode('utf-8')
# print("wwwwwwwwwwwwwwwwwwwww", type(page))  # <class 'str'>
# print("================",json.loads(page))  # <class 'list'>
