#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

from task_manage.my_ansible.run_adhoc import AdhocRunner
def main():
    

    temphosts_dict = {
        "Group1": {
            "hosts": [{"ip": "10.0.0.61", "port": "22", "username": "root", "password": "123456"}
                      ],
            "group_vars": {"var1": "ansible"}
        },
        # "Group2": {}
    }

    # mi = MyInventory(temphosts_list)
    # for group, hosts in mi.INVENTORY.get_groups_dict().items():
    #     print(group, hosts)
    # host = mi.INVENTORY.get_host("192.168.200.10")
    # print(mi.VARIABLE_MANAGER.get_vars(host=host))
    # Searched in:\n\t/project/CMDB/task_manage/my_ansible/files/10.0.0.61应用3
    tasks = []
    tasks.append(dict(action=dict(module="shell",
                                  args="tail -f /var/log/messages",
                                  warn=False)))
    tasks.append(dict(action=dict(module="script", args='/project/CMDB/tmp_dir/10.0.0.61应用1.sh', warn=False)))
    hosts = "Group1"
    ar = AdhocRunner(temphosts_dict)
    ar.run_adhoc(hosts, tasks)
    print("changed==============", ar.get_adhoc_result().get("changed"))
    print("status==============", ar.get_adhoc_result().get("status"))
    print("skipped==============", ar.get_adhoc_result().get("skipped"))
    print("failed==============", ar.get_adhoc_result().get("failed"))
    # failed有值的时候，ok中也是有堆值的
    # {'10.0.0.61': {'changed': True, 'end': '2019-07-29 16:30:25.023962', 'stdout': '', 'cmd': 'ech ansible', 'delta': '0:00:00.006034', 'stderr': '/bin/sh: ech: command not found', 'rc': 127, 'invocation': {'module_args': {'creates': None, 'executable': None, '_uses_shell': True, '_raw_params': 'ech ansible', 'removes': None, 'argv': None, 'warn': True, 'chdir': None, 'stdin': None}}, 'start': '2019-07-29 16:30:25.017928', 'msg': 'non-zero return code', '_ansible_parsed': True, 'stdout_lines': [], 'stderr_lines': ['/bin/sh: ech: command not found'], '_ansible_no_log': False}}
    # {'10.0.0.61': {'invocation': {'module_args': {'filter': '*', 'gather_subset': ['all'], 'fact_path': '/etc/ansible/facts.d', 'gather_timeout': 10}}, 'ansible_facts': {'ansible_product_serial': 'VMware-56 4d 75 36 4b f6 4a 8f-7c 47 ee 69 54 be 11 5d', 'ansible_form_factor': 'Other', 'ansible_user_gecos': 'root', 'ansible_distribution_file_parsed': True, 'ansible_fips': False, 'ansible_service_mgr': 'upstart', 'ansible_user_id': 'root', 'ansible_selinux_python_present': False, 'ansible_userspace_bits': '64',}
    print("ok==============", ar.get_adhoc_result().get("ok"))
    #  {'10.0.0.61': {'changed': True, 'end': '2019-07-29 16:27:31.279191', 'stdout': 'ansible', 'cmd': 'echo ansible', 'rc': 0, 'start': '2019-07-29 16:27:31.274105', 'stderr': '', 'delta': '0:00:00.005086', 'invocation': {'module_args': {'creates': None, 'executable': None, '_uses_shell': True, '_raw_params': 'echo ansible', 'removes': None, 'argv': None, 'warn': True, 'chdir': None, 'stdin': None}}, '_ansible_parsed': True, 'stdout_lines': ['ansible'], 'stderr_lines': [], '_ansible_no_log': False}}
    print("unreachable==============",ar.get_adhoc_result().get("unreachable"))
#     {'10.0.0.63': {'unreachable': True, 'msg': 'Failed to connect to the host via ssh: OpenSSH_5.3p1, OpenSSL 1.0.1e-fips 11 Feb 2013\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug1: Control socket "/root/.ansible/cp/b74d7cb4b9" does not exist\r\ndebug2: ssh_connect: needpriv 0\r\ndebug1: Connecting to 10.0.0.63 [10.0.0.63] port 22.\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug1: connect to address 10.0.0.63 port 22: Connection timed out\r\nssh: connect to host 10.0.0.63 port 22: Connection timed out', 'changed': False}}

if __name__ == "__main__":

    main()
