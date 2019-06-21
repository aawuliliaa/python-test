#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from wsgiref.simple_server import make_server
from urls import url_patterns
from views import *


def application(environ, start_response):
    path = environ.get("PATH_INFO")
    start_response("200 OK", [])
    func = None
    # url_patterns是一个列表，列表中的每项是一个数组
    for item in url_patterns:
        if path == item[0]:
            func = item[1]
            break

    if func:
        # 这种return []是wsgiref模块规定的模式
        return [func(environ)]
if __name__ == '__main__':

    # 启动socket服务，等待连接
    httpd = make_server("127.0.0.1", 8800, application)
    httpd.serve_forever()
