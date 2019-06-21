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
    for item in url_patterns:
        if path == item[0]:
            func = item[1]
            break

    if func:
        return [func(environ)]


httpd = make_server("127.0.0.1", 8800, application)
httpd.serve_forever()
