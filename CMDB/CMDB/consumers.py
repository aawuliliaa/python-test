from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        # 创建channels group， 命名为：用户名，并使用channel_layer写入到redis
        # 注意，这里我之前想用邮箱的，但是由于里面有@,debug调试时，发现不可以，报错提示没保留，所以就改用name了
        # 或者可以自己定义一个规范的字符串，防止报错
        # 如果定义一个固定的名字，那么不管哪个用户登录，一个用户点击查看日志，其他用户的这个页面也会跟着刷新，会互相影响
        # 我这里每个用户定义一个自己的组,就不会互相影响了
        async_to_sync(self.channel_layer.group_add)(self.scope['user'].name, self.channel_name)

        # 返回给receive方法处理
        self.accept()

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.scope['user'].name,
            {
                "type": "user.message",
                "text": text_data,
            },
        )

    def user_message(self, event):
        # 消费
        self.send(text_data=event["text"])

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.scope['user'].name, self.channel_name)


# class StatsConsumer(WebsocketConsumer):
#
#     def connect(self):
#         async_to_sync(self.channel_layer.group_add)(self.scope['user'].username, self.channel_name)
#
#         self.accept()
#
#     def receive(self, text_data):
#         key = '-'.join(('django-mstats-processlist', str(self.scope['user'].uid)))
#         cache.set(key, 'start', timeout=None)
#         show_processlist.delay(host=text_data, user=self.scope['user'].username, key=key)
#
#         async_to_sync(self.channel_layer.group_send)(
#             self.scope['user'].username,
#             {
#                 "type": "user.message",
#                 "text": text_data,
#             },
#         )
#
#     def user_message(self, event):
#         self.send(text_data=event["text"])
#
#     def disconnect(self, close_code):
#         key = '-'.join(('django-mstats-processlist', str(self.scope['user'].uid)))
#         cache.set(key, 'end', timeout=None)
#         async_to_sync(self.channel_layer.group_discard)(self.scope['user'].username, self.channel_name)