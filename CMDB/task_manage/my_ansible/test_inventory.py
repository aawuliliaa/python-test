#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from task_manage.my_ansible.my_inventory import MyInventory
from ansible.inventory.host import Host
from ansible.inventory.group import Group
def main():
    hosts_resource = {
            "Group1": {
                "hosts": [{"ip": "10.0.0.62", "port": "22", "username": "root", "password": "123456"},
                          {"ip": "10.0.0.61", "port": "22", "username": "root", "password": "123456"}],
                "group_vars": {"var1": "ansible"}
            },
            # "Group2": {}
        }
    my_inventory_obj = MyInventory(hosts_resource)
    print(my_inventory_obj.inventory_obj.get_groups_dict())

#     1.get_groups_dict()组信息：
#     如果配置了正确的sources, InventoryManager(loader=self.loader, sources=self.hosts_file),输出是
#     {'all': ['10.0.0.62', '172.16.1.61', '10.0.0.61'],
#     'ungrouped': ['10.0.0.61'], 'db': ['172.16.1.61'],
#     'php': ['172.16.1.61'], 'nginx': ['10.0.0.62'],
#     'Group1': ['10.0.0.62', '10.0.0.61']}
#      如果没有配置正确的sources,即self.hosts_file = [""] ，输出是
#  [WARNING]: No inventory was parsed, only implicit localhost is available
# {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61']}
# 想怎样配置，看自己需求啦，啦啦啦啦
    print(type(my_inventory_obj.inventory_obj.get_groups_dict()))
    # <class 'dict'>，组内的主机信息就通过操作字典来获取数据了
    # 2.获取主机对象
    print(my_inventory_obj.inventory_obj.get_hosts())  # []
    host = my_inventory_obj.inventory_obj.get_host("10.0.0.61")
    print()  # 10.0.0.61
    print(type(host))  # <class 'ansible.inventory.host.Host'>
    # 3.获取主机的变量
    print(host.get_vars())
    # {'ansible_port': 22, 'inventory_file': None, 'inventory_dir': None,
    # 'inventory_hostname': '10.0.0.61', 'inventory_hostname_short': '10', 'group_names': ['Group1']}
    print(type(host.get_vars()))  # <class 'dict'>
    # 4.获取主机所在的组
    print(host.get_groups())  # [Group1]
    print(type(host.get_groups()))  # <class 'list'>
    # 5.获取组对象
    group_obj = my_inventory_obj.inventory.groups.get("Group1")
    # group_obj = Group(name="Group2")
    print(type(group_obj))  # <class 'ansible.inventory.group.Group'>
    # 6.把主机添加到组中，但这样并没有添加到inventory中
    my_inventory_obj.inventory.add_group("Group2")
    group_obj2 = my_inventory_obj.inventory.groups.get("Group2")
    new_host = Host(name="10.0.0.63", port="22")
    new_host.add_group(group_obj2)
    print(new_host.groups)  # [Group2]
    print(my_inventory_obj.inventory.get_groups_dict())
    # {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61'], 'Group2': []}
    # 添加主机到主机组
    # 添加主机到主机组
    my_inventory_obj.inventory.add_host(host="10.0.0.63", group="Group2", port="22")
    print(my_inventory_obj.inventory.get_groups_dict())
    # {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61'], 'Group2': ['10.0.0.63']}

    # 7.获取主机的变量
    print(my_inventory_obj.variable_manager.get_vars(host=host))
#     {'var1': 'ansible', 'ansible_port': 22, 'inventory_file': None, 'inventory_dir': None,
#     'inventory_hostname': '10.0.0.61', 'inventory_hostname_short': '10',
#     'group_names': ['Group1'], 'ansible_facts': {}, 'ansible_ssh_host': '10.0.0.61', 'ansible_ssh_port': '22',
#     'ansible_ssh_user': 'root', 'ansible_ssh_pass': '123456',
#     'playbook_dir': '/project/CMDB/task_manage/my_ansible',
#     'ansible_playbook_python': '/usr/bin/python3',
#     'groups': {'all': [], 'ungrouped': [], 'Group1': ['10.0.0.62', '10.0.0.61'], 'Group2': []},
#     'omit': '__omit_place_holder__3a96c0f711c926b0ece7e5caf5d969d656ddfbe0'}


if __name__ == '__main__':
    main()