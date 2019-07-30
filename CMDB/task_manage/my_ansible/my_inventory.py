#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: vita


# 用于读取YAML和JSON格式的文件
from ansible.parsing.dataloader import DataLoader
# 用于存储各类变量信息
from ansible.vars.manager import VariableManager
# 用于导入资产文件
from ansible.inventory.manager import InventoryManager
# 操作单个主机信息
from ansible.inventory.host import Host
# 操作单个主机组信息
# from ansible.inventory.group import Group


class MyInventory:
    """
    动态生成/etc/ansible/hosts文件
    """
    def __init__(self, hosts_resource):
        #  hosts_resource = {
        #         "Group1": {
        #             "hosts": [{"ip": "10.0.0.62", "port": "22", "username": "root", "password": "123456"},
        #                       {"ip": "10.0.0.61", "port": "22", "username": "root", "password": "123456"}],
        #             "group_vars": {"var1": "ansible"}
        #         },
        #         # "Group2": {}
        #     }
        self.hosts_resource = hosts_resource
        self.loader = DataLoader()
        self.hosts_file = [""]
        """
        sources这个我们知道这里是设置hosts文件的地方，它可以是一个列表里面包含多个文件路径且文件真实存在，在单纯的执行ad-hoc的时候这里的
        文件里面必须具有有效的hosts配置，但是当通过动态生成的资产信息的时候这个文件必须存在但是它里面可以是空的，如果这里配置成None那么
        它不影响资产信息动态生成但是会有一个警告
         [WARNING]: No inventory was parsed, only implicit localhost is available

         {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61']}
        """
        self.inventory = InventoryManager(loader=self.loader, sources=self.hosts_file)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.dynamic_inventory()

    def add_hosts_group(self, hosts_list, group_name, group_vars=None):
        """
        动态添加主机到指定的主机组

        完整的HOSTS文件格式
        [test1]
        hostname ansible_ssh_host=192.168.1.111 ansible_ssh_user="root" ansible_ssh_pass="123456"

        但通常我们都省略hostname，端口也省略因为默认是22，这个在ansible配置文件中有，除非有非22端口的才会配置
        [test1]
        192.168.100.10 ansible_ssh_user="root" ansible_ssh_pass="123456" ansible_python_interpreter="/usr/bin/python3"
        [test2]
        192.168.100.10 ansible_ssh_user="root" ansible_ssh_pass="123456" ansible_python_interpreter="/usr/bin/python3"
        [parent_group:children]
        test1
        test2
        [test2:vars]
        touch_file=new_file
        :param hosts_list: 主机列表 [{"hostname":"m01","ip": "192.168.100.10", "port": "22",
                                     "username": "root", "password": None}, {}]
        :param group_name:  组名称
        :param group_vars:  组变量，格式为字典group_vars={"var1": "ansible"}
        :return:
        """
        # 如果主机组不存在，就添加主机组，如果存在，就直接获取
        if not self.inventory.groups.get(group_name):
            self.inventory.add_group(group_name)
        # 返回值是Group对象，注意这里一定要保证是同一个对象
        inventory_group = self.inventory.groups.get(group_name)
        # 如果组变量存在，就设置组变量，可用于playbook中
        if group_vars:
            for key, value in group_vars.items():
                inventory_group.set_variable(key, value)
        for host in hosts_list:
            ip = host.get("ip", None)
            hostname = host.get("hostname", ip)
            port = host.get("port", "22")
            username = host.get("username")
            password = host.get("password", None)
            ssh_key = host.get("ssh_key", None)
            python_interpreter = host.get("python_interpreter", None)

            try:
                host_obj = Host(name=hostname, port=port)
                self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_host", value=ip)
                self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_port", value=port)
                self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_user", value=username)
                if password:
                    self.variable_manager.set_host_variable(host=host_obj,
                                                            varname="ansible_ssh_pass",
                                                            value=password)
                if ssh_key:
                    self.variable_manager.set_host_variable(host=host_obj,
                                                            varname="ansible_ssh_private_key_file",
                                                            value=ssh_key)
                if python_interpreter:
                    self.variable_manager.set_host_variable(host=host_obj,
                                                            varname="ansible_python_interpreter",
                                                            value=python_interpreter)

                # 添加其他变量
                for key, value in host.items():
                    if key not in ["ip", "hostname", "port", "username", "password", "ssh_key", "python_interpreter"]:
                        self.variable_manager.set_host_variable(host=host_obj, varname=key, value=value)

                # 添加主机到主机组
                self.inventory.add_host(host=hostname, group=group_name, port=port)
            except Exception as e:
                print(e)

    def dynamic_inventory(self):
        # 为了以后扩展，我们先把该段内容写在这里
        for group_name, hosts_and_vars in self.hosts_resource.items():
            self.add_hosts_group(hosts_and_vars.get("hosts"), group_name, hosts_and_vars.get("group_vars"))

    @property
    def inventory_obj(self):
        """
        返回inventory對象
        :return:
        """
        return self.inventory

    @property
    def variable_manager_onj(self):
        """
       返回variable_manager對象
       :return:
       """
        return self.variable_manager
