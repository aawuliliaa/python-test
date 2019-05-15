#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from core.ftpserver import FtpServer
from utils.print_write_log import print_info


class Management(object):
    def __str__(self):
        return "to manage ftp server"

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

    def __print_help_msg(self):
        """
        打印启动的帮助信息,只是内部使用，不对外使用，可以设置为隐藏函数
        :return:
        """
        help_msg = """
        [python run_server.py start] to start ftp server!
        [python run_server.py stop] to stop ftp server!
        """
        print_info(help_msg)


    def start(self):
        ftp_server_obj = FtpServer()
        ftp_server_obj.keep_running()
