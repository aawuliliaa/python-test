#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: vita

# 用于读取YAML和JSON格式的文件
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from collections import namedtuple
from task_manage.my_ansible.my_inventory import MyInventory
from task_manage.my_ansible.result_call_back import CallbackResultCollector
class PlaybookRunner(object):
    def __init__(self, hostsresource):
        Options = namedtuple("Options", [
            "connection", "remote_user", "ask_sudo_pass", "verbosity", "ack_pass",
            "module_path", "forks", "become", "become_method", "become_user", "check",
            "listhosts", "listtasks", "listtags", "syntax", "sudo_user", "sudo", "diff"
        ])
        self._options = Options(connection='smart', remote_user=None, ack_pass=None, sudo_user=None, forks=5, sudo=None,
                          ask_sudo_pass=False,
                          verbosity=5, module_path=None, become=None, become_method=None, become_user=None, check=False,
                          diff=False,
                          listhosts=None, listtasks=None, listtags=None, syntax=None)
        self._passwords = dict(sshpass=None, becomepass=None)  # 这个可以为空，因为在hosts文件中
        self._loader = DataLoader()
        myinven = MyInventory(hosts_resource=hostsresource)
        self._inventory = myinven.inventory_obj
        self._variable_manager = myinven.variable_manager_obj

    def run_playbook(self, playbook_path, extra_vars=None):
        """
        执行playbook
        :param playbook_path: playbook的yaml文件路径
        :param extra_vars: 额外变量
        :return: 无返回值
        """
        try:
            if extra_vars:
                self._variable_manager.extra_vars = extra_vars
            playbook = PlaybookExecutor(playbooks=[playbook_path], inventory=self._inventory,
                                        variable_manager=self._variable_manager, loader=self._loader,
                                        options=self._options, passwords=self._passwords)
            # 配置使用自定义callback
            self._callback = CallbackResultCollector()
            playbook._tqm._stdout_callback = self._callback
            # 执行playbook
            playbook.run()
        except Exception as err:
            print(err)

    def get_playbook_result(self):
        """
        获取playbook执行结果
        :return:
        """
        result_raw = {"ok": {}, "failed": {}, "unreachable": {}, "skipped": {}, "status": {}}
        for host, result in self._callback.task_ok.items():
            result_raw["ok"][host] = result._result

        for host, result in self._callback.task_failed.items():
            result_raw["failed"][host] = result._result

        for host, result in self._callback.task_unreachable.items():
            result_raw["unreachable"][host] = result._result

        for host, result in self._callback.task_skipped.items():
            result_raw["skipped"][host] = result._result

        for host, result in self._callback.task_status.items():
            result_raw["status"][host] = result._result

        return result_raw