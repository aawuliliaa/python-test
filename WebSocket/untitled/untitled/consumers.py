#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from testchannel.tasks import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 连接时触发
        self.group_name = "chat_group"
        await  self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        await self.accept()
    async def disconnect(self, code):
        # 关闭连接时触发
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )
        pass
    async def receive(self, text_data=None, bytes_data=None):
        # 收到消息后触发
        # 真个ChatConsumer类会将所有接收到的消息加上一个"聊天"的前缀发送给客户端
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("wwwwwwwwwwwww", message)# yyyyyyyyyyyyy
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message':message
            }
        )
    async def chat_message(self,event):
        print("enventooooooooooooooooo",event) # {'type': 'chat_message', 'message': 'yyyyyyyyyyyyy'}
        message = "聊天:" + event["message"]
        await self.send(text_data=json.dumps({'message':message}))

class TailfConsumer(WebsocketConsumer):
    def connect(self):
        self.file_id = self.scope["url_route"]["kwargs"]["id"]
        self.result = tailf.delay(self.file_id,self.channel_name)
        # self.result = add.delay(1,8)
        self.accept()
    def disconnect(self, code):
        self.result.revoke(terminate=True)
    def send_message(self,event):
        self.send(text_data=json.dumps({"message":event["message"]}))
