#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import socket
import json
import os
import configparser
from conf import settings
from utils.print_write_log import print_info


class FtpServer(object):
    MSG_SIZE = 1024
    STATUS_CODE = {
        "100": "login success!",
        "101": "your password is not correct",
        "102": "user not exist"
    }

    def __init__(self):
        self.server_socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_conn_obj = None
        self.client_addr = None
        self.accounts = self.load_accounts()
        self.user_current_dir = None
    @staticmethod
    def load_accounts():
        """
        加载用户文件
        :return:
        """
        config_obj = configparser.ConfigParser()
        config_obj.read(settings.ACCOUNT_FILE)
        return config_obj

    def keep_running(self):
        """
        这里是允许多用户登录，但这里没有使用多线程，是通过while True的方式，
        一个用户断开连接，另一个用户才能继续连接
        :return:
        """
        self.server_socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket_obj.bind((settings.FTP_SERVER_HOST, settings.FTP_SERVER_PORT))
        self.server_socket_obj.listen(5)
        while True:
            print("waiting client to connect!")
            self.request_conn_obj, self.client_addr = self.server_socket_obj.accept()

            print_info("client connect:", self.client_addr)
            try:
                self.handle_client_request()
            except OSError as e:
                print(e)
            print("%s client closed connection!" % self.client_addr)

    def get_response_from_client(self):
        """
        接收客户端发送的数据
        :return:
        """
        # 客户端发送请求命令时，把数据封装为1024字节，避免粘包问题
        client_request_cmd = self.request_conn_obj.recv(self.MSG_SIZE)

        # 因为客户端是先dumps,然后encode("utf-8")
        client_request_cmd = json.loads(client_request_cmd.decode("utf-8"))
        #         client_request_cmd = {
        #             'action_type': action_type,
        #             'fill':''
        #         }
        return client_request_cmd

    def handle_client_request(self):
        """
        接收用户请求，并处理
        :return:
        """
        while True:
            client_request_cmd = self.get_response_from_client()
            action_type = client_request_cmd["action_type"]
            if hasattr(self, action_type):
                func = getattr(self, action_type)
                func(client_request_cmd)

    def send_certain_size_response(self, response_code, **kwargs):
        """
        发送固定打下的包到客户端，这是处理粘包问题的必备思路
        首先发送一个固定大小的包到对方，对方会按照指定大小接受，如果是文件，数据包中会含有要发送的文件的大小
        后面再发送文件或其他内容，对方只需要知道文件的大小，通过循环，即可接受全部的内容
        :param response_code:
        :param kwargs:
        :return:
        """
        response_data = {
            "fill": "",
            "response_code": response_code,
            "response_msg": self.STATUS_CODE[response_code]
        }

        response_data.update(kwargs)
        bytes_response_data = json.dumps(response_data).encode("utf-8")
        if len(bytes_response_data) < self.MSG_SIZE:
            # 进行数据填充，使得长度为1024字节
            response_data["fill"] = response_data["fill"].zfill(self.MSG_SIZE-len(bytes_response_data))
            bytes_response_data = json.dumps(response_data).encode("utf-8")
        # 这里一定是self.request_conn_obj，不是self.server_socket_obj
        self.request_conn_obj.send(bytes_response_data)

    def auth(self, client_request_cmd):
        """
        用户登录验证
        :param client_request_cmd:
        :return:
        """
        username = client_request_cmd["username"]
        password = client_request_cmd["password"]

        if username in self.accounts:
            real_password = self.accounts[username]["password"]
            if password == real_password:
                self.user_current_dir = os.path.join(settings.ACCOUNT_FILE, username)
                self.send_certain_size_response("100")

            else:
                print_info("your password is not correct", "error")
                self.send_certain_size_response("101")
        else:
            print_info("user %s not exist" % username, "error")
            self.send_certain_size_response("102")

    def put(self):
        pass
    def get(self):
        pass
    def ls(self):
        pass
    def cd(self):
        pass
