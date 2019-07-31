#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path,re_path
from untitled.consumers import *

websocket_urlpatterns = [
    path(r"ws/chat/", ChatConsumer),
    re_path(r'^ws/tailf/(?P<id>\d+)/$', TailfConsumer),
]

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

