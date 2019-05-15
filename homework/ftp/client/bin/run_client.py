#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import socket
import optparse
import json
from utils.print_write_log import print_info


class FtpClient(object):
    MSG_SIZE = 1024

    def __init__(self):
        self.client_socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.options = None
        self.args = None
        self.terminal_display = None
        self.verify_args()
        self.connect_to_server()

    def verify_args(self):
        parser = optparse.OptionParser()
        # python.exe run_client.py -s 127.0.0.1 -P 9999
        # (<Values at 0x1b9dd3a5128: {'server': '127.0.0.1', 'port': '9999'}>, [])
        parser.add_option("-s", "--server", dest="server", help="ftp server ip")
        parser.add_option("-P", "--port", dest="port", help="ftp server port")
        self.options, self.args = parser.parse_args()
        # {'server': None, 'port': None} <class 'optparse.Values'> []
        # print(self.options,type(self.options),self.args)
        if not self.options.server or not self.options.port:

            exit("python run_client.py -s ftp_server_ip -P ftp_server_port")

    def connect_to_server(self):
        """
        根据IP和port连接到ftp服务端
        :return:
        """
        server_ip = self.options.server
        server_port = int(self.options.port)
        self.client_socket_obj.connect_ex((server_ip, server_port))

    def interactive(self):
        """
        与用户交互的方法
        :return:
        """
        if self.auth():
            while True:
                client_cmd = input(">>")

    def get_response_from_server(self):
        """
        接收从服务端发送的数据，并对数据解析，然后返回数据
        :return:
        """
        response_data = self.client_socket_obj.recv(self.MSG_SIZE)
        response_data = json.loads(response_data.decode("utf-8"))
        return response_data

    def auth(self):
        """
        用户登录方法，首先是用户登录，登录成功后才能进行后面的操作
        :return:
        """
        count = 0
        while count < 3:
            username = input("please input username:").strip()
            password = input("please input password:").strip()
            if username and password:
                # 发送用户名和密码到服务端
                self.send_certain_size_msg("auth", username=username, password=password)
                response_data = self.get_response_from_server()
                if response_data["response_code"] == "100":
                    print_info(response_data["response_msg"])
                    self.terminal_display = "[%s]" % username
                    return True
                else:
                    print_info(response_data["response_msg"], "error")
                    count += 1
            else:
                print_info("username or password an not be null!", "error")
                count += 1
        return False
    def send_certain_size_msg(self,action_type,**kwargs):
        """
        发送固定打下的包到服务端，这是处理粘包问题的必备思路
        首先发送一个固定大小的包到对方，对方会按照指定大小接受，如果是文件，数据包中会含有要发送的文件的大小
        后面再发送文件或其他内容，对方只需要知道文件的大小，通过循环，即可接受全部的内容
        :param action_type:
        :param kwargs:
        :return:
        """
        msg_data = {"action_type": action_type,
                    "fill": ""}
        # 更新msg_data字典，因为可能会加入新的key,value放入到了kwargs中
        msg_data.update(kwargs)
        bytes_msg_data = json.dumps(msg_data).encode("utf-8")
        # 为了避免粘包问题，每次首先都发送一个定长的数据(这里定长为1024字节，足够使用了)到服务端，
        # 服务端根据这个数据中的信息进行后面的操作
        if len(bytes_msg_data) < self.MSG_SIZE:
            # 进行数据填充，使得长度为1024字节
            msg_data["fill"] = msg_data["fill"].zfill(self.MSG_SIZE-len(bytes_msg_data))
            bytes_msg_data = json.dumps(msg_data).encode("utf-8")
        self.client_socket_obj.send(bytes_msg_data)
        print_info("your commands has send to ftp server successful!")

if __name__ == '__main__':
    ftp_client_obj = FtpClient()
    ftp_client_obj.interactive()