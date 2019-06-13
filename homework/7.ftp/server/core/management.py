#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import subprocess
import re
from core.ftpserver import FtpServer
from utils.print_write_log import print_info


class Management(object):
    def __str__(self):
        return "to manage 7.ftp server"

    def __init__(self, sys_args):
        # 用于接收脚本的参数
        self.sys_args = sys_args
        pass

    def run(self):
        """
        入口程序
        :return:
        """
        # 客户执行启动或停止的命令是在启动脚本后加 start 或stop，多参数或少参数都要报错
        if len(self.sys_args) != 2:
            self.__print_help_msg()

        else:
            # 只有在有一个参数的时候，即符合启动的命令，才进行下面的判断
            if hasattr(self, self.sys_args[1]):
                func = getattr(self, self.sys_args[1])
                func()
            else:
                self.__print_help_msg()

    @staticmethod
    def __print_help_msg():
        """
        打印启动的帮助信息,只是内部使用，不对外使用，可以设置为隐藏函数
        :return:
        """
        help_msg = """
        [python run_server.py start] to start 7.ftp server!
        [python run_server.py stop] to stop 7.ftp server!
        """
        print_info(help_msg)

    @staticmethod
    def start():
        ftp_server_obj = FtpServer()
        ftp_server_obj.keep_running()

    @staticmethod
    def stop():
        cmd_obj = subprocess.Popen('tasklist|findstr "python"', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        stderr = cmd_obj.stderr.read()
        pid_console_list = re.findall("[0-9]+[ ]Console", (stdout+stderr).decode("gbk"))

        if pid_console_list:

            for pid_Console in pid_console_list:
                pid = int(re.search("[0-9]+", pid_Console).group())
                # print(pid.group(),type(pid.group()))
                kill_cmd_obj = subprocess.Popen('taskkill /PID %s -t -f' % pid, shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                kill_stdout = kill_cmd_obj.stdout.read()
                kill_stderr = kill_cmd_obj.stderr.read()
                print((kill_stderr + kill_stdout).decode("gbk"))
