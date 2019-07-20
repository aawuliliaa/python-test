#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from urllib.parse import parse_qs
from models import get_data
from django.urls import reverse


def index(environ):
    with open("./templates/index.html","rb") as f:
        data = f.read()
    return data


def login(environ):
    with open("./templates/login.html", "rb") as f:
        data = f.read()
    return data


def favicon(environ):
    with open("./templates/favicon.ico", "rb") as f:
        data = f.read()
    return data

def auth(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    data = parse_qs(request_body)
    # 我这个是windows系统，所以这里要以gbk解码，如果是linux或mac,要用utf8解码
    # 获取页面上的用户名和密码
    user = data.get(b"user")[0].decode("gbk")
    pwd = data.get(b"pwd")[0].decode("gbk")

    cur = get_data(user, pwd)
    # 如果用户名，密码正确，就展示index页面
    if cur.fetchone():
        return index(environ)
    else:
        return b'user or pwd is wrong!'


