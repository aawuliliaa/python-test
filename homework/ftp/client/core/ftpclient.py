#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import socket
import optparse
import json
import os
import re
import subprocess
from utils.print_write_log import print_info
from conf import settings


class FtpClient(object):
    MSG_SIZE = 1024

    def __init__(self):
        self.client_socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.options = None
        self.args = None
        self.username = None
        # 可展示出用户当前所在目录
        self.terminal_display = None
        self.verify_args()
        self.connect_to_server()
        self.left_quota = None

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
        exit_flag = True
        while exit_flag:
            info = """
            1.创建用户
            2.登录
            3.退出
            """
            choice_list = {
                "1": "create_user",
                "2": "login",
                "3": "quit"
            }
            print_info(info)
            your_choice = input("please input your choice:").strip()
            if your_choice in choice_list:
                if choice_list[your_choice] == "quit":
                    self.quit([])
                else:
                    func = getattr(self, choice_list[your_choice])
                    func()

    def create_user(self):
        exit_flag = True
        while exit_flag:
            new_user_name = input("please input new user name:").strip()
            new_user_password = input("please set user password:").strip()
            user_quota = input("please set user quota[G]:").strip()
            # 验证用户的输入是否标准
            # 其中用户配额，由于单位过多，所以这里只能存G，服务端会进行转换为字节
            # 这里会验证用户配额输入的否标准
            if new_user_name and new_user_password and user_quota.endswith("G") \
                    and user_quota.replace("G", "").replace(".", "").isdigit():
                self.send_certain_size_msg("create_user",
                                           new_user_name=new_user_name,
                                           new_user_password=new_user_password,
                                           user_quota=user_quota)
                response_data = self.get_response_from_server()
                if response_data["response_code"] == "500":
                    print_info(response_data["response_msg"])
                    exit_flag = False
                else:
                    print_info(response_data["response_msg"])
                    exit_flag = False

            else:
                print_info("your input is illegal!")
                exit_flag = False

    def login(self):
        if self.auth():
            while True:
                # 用户输入ls, get file ,put file,cd dir
                print_info("you can input [quit] to exit client!")
                client_cmd = input("your input %s#" % self.terminal_display).strip()
                if not client_cmd:
                    continue
                client_cmd_list = client_cmd.split()
                # 用户输入的第一个命令
                if hasattr(self, client_cmd_list[0]):
                    func = getattr(self, client_cmd_list[0])
                    # 把后面的内容传给方法
                    func(client_cmd_list[1:])

    @staticmethod
    def verify_client_cmd_list(client_cmd_list, exact_arg_num):
        if len(client_cmd_list) != exact_arg_num:
            return False
        return True

    def quit(self, client_cmd_list):
        """
        退出客户端,用户只能输入quit，所以len(cmd_list)==0
        :return:
        """

        if self.verify_client_cmd_list(client_cmd_list, 0):
            self.send_certain_size_msg("quit")
            print_info("%s waiting for you come again! bye bye!" % self.username)
            exit()
        else:
            print_info("your input is illegal!you can just input [quit]!", "error")

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
                    self.username = username
                    self.left_quota = response_data["left_quota"]
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

    @staticmethod
    def progress_bar(file_total_size, last_percent=0):

        while True:
            # 每次接收完成传送的文件大小
            finished_file_size = yield
            current_percent = int(finished_file_size / file_total_size * 100)
            # 这里不能使用if finished_file_size < file_total_size
            # 因为 类似这种，相同百分比会打印好几次，下面这种判断可以避免这种现象
            # ###########################################86%
            # ###########################################86%
            # ###########################################86%
            # ###########################################86%
            if current_percent > last_percent:
                print("#" * int(current_percent / 2) + "{percent}%".format(percent=current_percent), end='\r',
                      flush=True)
                last_percent = current_percent  # 把本次循环的percent赋值给last

    @staticmethod
    def file_md5_value(file_asb_path):
        cmd_obj = subprocess.Popen(
            "certutil -hashfile %s MD5" % file_asb_path,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        # stderr = cmd_obj.stderr.read()
        # print(stdout.decode("gbk"))
        file_md5_value = re.findall("[0-9a-zA-Z]{32}", stdout.decode("gbk"))[0]
        return file_md5_value

    def put(self, client_cmd_list):
        """
        这里就只允许用户上传所在系统的任意文件，但是需要写出绝对路径
        :param client_cmd_list:
        :return:
        """
        if self.verify_client_cmd_list(client_cmd_list, 1):
            file_abs_path = client_cmd_list[0]
            # 获取md5值，用于验证数据的准确性
            file_md5_value = self.file_md5_value(file_abs_path)
            if os.path.isfile(file_abs_path):
                file_total_size = os.path.getsize(file_abs_path)
                # 先把文件的信息发送到服务端，然后在发送文件的内容
                if self.left_quota > file_total_size:
                    file_name = os.path.basename(file_abs_path)
                    self.send_certain_size_msg("put", file_total_size=file_total_size, file_name=file_name,
                                               file_md5_value=file_md5_value)
                    f = open(file_abs_path, "rb")
                    finished_file_size = 0
                    progress_generator = self.progress_bar(file_total_size)
                    progress_generator.__next__()
                    for line in f:
                        self.client_socket_obj.send(line)
                        finished_file_size += len(line)
                        progress_generator.send(finished_file_size)
                    f.close()
                    self.left_quota -= file_total_size
                    print_info("\nfile transfer finished!")
                else:
                    print_info("left quota is not enough!")
            else:
                print_info("your put file is not a file!")
        else:
            print_info("your input is illegal!for example [put e:\\file.txt]")

    def get(self, client_cmd_list):
        """
        从服务端下载文件，保存到客户端的file_storage路径下，包含md5验证
        :param client_cmd_list:
        :return:
        """
        if self.verify_client_cmd_list(client_cmd_list, 1):
            # get a/b/test.txt会从服务端的当前所在路径下的a/b/中获取test.txt
            file_relative_path = client_cmd_list[0]
            file_name = os.path.basename(file_relative_path)
            # 存放文件的路径，放在storage下
            file_storage_path = os.path.join(settings.FILE_STORAGE_PATH, file_name)
            self.send_certain_size_msg("get",  file_relative_path=file_relative_path)
            response_data = self.get_response_from_server()
            if response_data["response_code"] == "200":
                print_info(response_data["response_msg"])
                file_total_size = response_data["file_total_size"]
                source_file_md5_value = response_data["file_md5_value"]
                f = open(file_storage_path, "wb")
                received_file_size = 0
                progress_bar = self.progress_bar(file_total_size)
                progress_bar.__next__()
                while received_file_size < file_total_size:
                    left_file_size = file_total_size - received_file_size
                    if left_file_size < self.MSG_SIZE:
                        data = self.client_socket_obj.recv(left_file_size)
                        # 这样操作是不可以的len(data)!=left_file_size
                        # received_file_size += left_file_size
                    else:
                        data = self.client_socket_obj.recv(self.MSG_SIZE)
                        # received_file_size += self.MSG_SIZE
                    received_file_size += len(data)
                    progress_bar.send(received_file_size)
                    f.write(data)

                f.close()
                file_md5_value = self.file_md5_value(file_storage_path)
                if source_file_md5_value == file_md5_value:
                    print_info("\n file is same with sever,file download successful!")
                else:
                    print_info("\n file is not same with server!", "error")
            else:
                print_info(response_data["response_msg"])
        else:
            print_info("your input is illegal!for example [get file.txt]")

    def ls(self, client_cmd_list):
        """
        列出用户当前目录下的内容，当前目录是以服务端的self.user_current_dir为准
        :param client_cmd_list:
        :return:
        """
        if self.verify_client_cmd_list(client_cmd_list, 0):
            self.send_certain_size_msg("ls")
            response_data = self.get_response_from_server()
            if response_data["response_code"] == "300":
                print_info(response_data["response_msg"])
                cmd_result_total_size = response_data["cmd_result_total_size"]
                received_file_size = 0

                while received_file_size < cmd_result_total_size:
                    left_file_size = cmd_result_total_size - received_file_size
                    if left_file_size < self.MSG_SIZE:
                        data = self.client_socket_obj.recv(left_file_size)
                        # 这样操作是不可以的len(data)!=left_file_size
                        # received_file_size += left_file_size
                    else:
                        data = self.client_socket_obj.recv(self.MSG_SIZE)
                        # received_file_size += self.MSG_SIZE
                    received_file_size += len(data)
                    print_info(data.decode("gbk"))
        else:
            print_info("your input is illegal!for example [ls ]")

    def cd(self,client_cmd_list):
        """
        cd a/b 由于用户只能在自己的家目录下下切换，所以会把用户输入的目录与服务端的user_current_dir拼
        :param client_cmd_list:
        :return:
        """
        if self.verify_client_cmd_list(client_cmd_list, 1):
            target_path = client_cmd_list[0]
            self.send_certain_size_msg("cd", target_path=target_path)
            response_data = self.get_response_from_server()
            if response_data["response_code"] == "400":
                client_terminal_display_dir = response_data["client_terminal_display_dir"]
                if len(client_terminal_display_dir) == 0:
                    self.terminal_display = "[%s]" % self.username
                else:
                    self.terminal_display = "[%s]" % client_terminal_display_dir
                print_info("change dir success!")
            else:
                print_info(response_data["response_msg"])
        else:
            print_info("your input is illegal!for example [cd a/b ]")