#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # 连接时触发
        self.accept()
    def disconnect(self, code):
        # 关闭连接时触发
        pass
    def receive(self, text_data=None, bytes_data=None):
        # 收到消息后触发
        # 真个ChatConsumer类会将所有接收到的消息加上一个"聊天"的前缀发送给客户端
        text_data_json = json.loads(text_data)
        message = "聊天:"+text_data_json["message"]
        self.send(text_data=json.dumps({"message":message}))