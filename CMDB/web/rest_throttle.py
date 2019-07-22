#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from rest_framework.throttling import SimpleRateThrottle


class MyThrottle(SimpleRateThrottle):
    """
    设置访问频率
    超过访问频率，会报错
    urllib.error.HTTPError: HTTP Error 429: Too Many Requests
    """
    scope = "WD"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
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
