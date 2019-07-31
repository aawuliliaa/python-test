#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # 连接时触发
        self.group_name = "chat_group"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()
    def disconnect(self, code):
        # 关闭连接时触发
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        pass
    def receive(self, text_data=None, bytes_data=None):
        # 收到消息后触发
        # 真个ChatConsumer类会将所有接收到的消息加上一个"聊天"的前缀发送给客户端
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message':message
            }
        )
    def chat_message(self,event):
        message = "聊天:" + event["message"]
        self.send(text_data=json.dumps({'message':message}))