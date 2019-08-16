# #消费者是一种阻塞模式，会一致取数据
# import pika
#
# credentials = pika.PlainCredentials('admin', '123456')  # 配置认证的用户 密码
# parameters = pika.ConnectionParameters(host="10.0.0.61", credentials=credentials)
# connection = pika.BlockingConnection(parameters)  # 建立一个链接对象
# channel = connection.channel()  # 队列连接通道
# channel.queue_declare(queue='hello')  # 声明queue 用rabbitmqctl list_queuses 查看
#
# def callback(ch, method, properties, body):
#     print("ch----------------------", ch)
#     print("method------------------", method)
#     print("properties--------------", properties)
#     print("body--------------------", body)
# # ch---------------------- <BlockingChannel impl=<Channel number=1 OPEN conn=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x00000241DB267E48> params=<ConnectionParameters host=10.0.0.61 port=5672 virtual_host=/ ssl=False>>>>
# # method------------------ <Basic.Deliver(['consumer_tag=ctag1.5efbc0dfd33e48ffb50889a7c3e1b292', 'delivery_tag=1', 'exchange=', 'redelivered=False', 'routing_key=hello'])>
# # properties-------------- <BasicProperties>
# # body-------------------- b'server hello world'
#
# channel.basic_consume('hello',# 队列名，从这个队列中取消息
#                       callback ,# 取到消息后，执行这个函数
#                       True,
#                       )
# print("waiting for message")
# channel.start_consuming()  # 进入阻塞模式，服务端发送一次，他就节后首一次


# 1.声明一个队列，作为reply_to返回消息结果的队列
# 2.  发消息到队列，消息里带一个唯一标识符uid，reply_to
# 3.  监听reply_to 的队列，直到有结果
import queue
import pika
import uuid


class CMDRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('admin', '123456')
        parameters = pika.ConnectionParameters(host='10.0.0.61', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='rpc_queue2')
        self.callback_queue = result.method.queue  # 命令的执行结果的queue

        # 声明要监听callback_queue
        self.channel.basic_consume(self.callback_queue, self.on_response, True)

    def on_response(self, ch, method, props, body):
        """
        收到服务器端命令结果后执行这个函数
        :param ch:
        :param method:
        :param props: 服务器端返回的消息结果！
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id:
            self.response = body.decode("gbk")  # 把执行结果赋值给Response

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())  # 唯一标识符号
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue2',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,  # 传递要返回的消息队列
                                       correlation_id=self.corr_id,  # 唯一id
                                   ),
                                   body=str(n))
        # 循环监听
        while self.response is None:
            self.connection.process_data_events()  # 检测监听的队列里有没有新消息，如果有，收，如果没有，返回None
            # 检测有没有要发送的新指令
        return self.response


cmd_rpc = CMDRpcClient()

print(" [x] Requesting fib(30)")
response = cmd_rpc.call('dir')
print(response)