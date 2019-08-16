#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
# import pika
#
# credentials = pika.PlainCredentials('admin', '123456')  # 配置认证的用户 密码
# parameters = pika.ConnectionParameters(host="10.0.0.61", credentials=credentials)
# connection = pika.BlockingConnection(parameters)  # 建立一个链接对象
# channel = connection.channel()  # 队列连接通道
#
# channel.queue_declare(queue='hello')  # 声明队列queue 用rabbitmqctl list_queuse 查看
# channel.basic_publish(exchange='', routing_key='hello', body='server hello world')  # routing_key 路由代表要发送的队列 body是发送的内容
# print('server send "hello world"')
# connection.close()  # 关闭连接 类似socket


import subprocess
import pika
import time

credentials = pika.PlainCredentials('admin', '123456')

parameters = pika.ConnectionParameters(host="10.0.0.61", credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()  # 队列连接通道

channel.queue_declare(queue='rpc_queue2')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def run_cmd(cmd):
    cmd_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = cmd_obj.stdout.read() + cmd_obj.stderr.read()

    return result


def on_request(ch, method, props, body):
    cmd = body.decode("utf-8")

    print(" [.] run (%s)" % cmd)
    response = run_cmd(cmd)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,  # 队列 接收客户端传过来的队列，返回
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume('rpc_queue2',on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()