# -*- coding: utf-8 -*-

from celery.task import task
import os
import random
from concurrent.futures import ThreadPoolExecutor
from django_celery_results.models import TaskResult
from threading import currentThread
from celery import shared_task
from asset.models import Host
from CMDB.settings import MAX_POOL_SIZE, BASE_DIR
from web.password_crypt import decrypt_p
from task_manage.my_ansible.run_adhoc import AdhocRunner
from asset.models import Host
# 自定义要执行的task任务
# 一定要加上name,否则会报错Received unregistered task_manage
# 在我这个版本整体中，不能使用@app.task_manage
@shared_task(name="add")
def add(x, y):
    return x+y


def get_host_info_func(host_set_list):
    """
    首先ansible远程操作主机，然后得到返回结果，把结果存到task_result表中，
    然后获取到的主机信息，如果有更新，就更新Host表
    :param host_set_list:
    :return:
    """
    result = {}
    # host_set_list = [<QuerySet [<Host: 10.0.0.61>]>]
    host_set = host_set_list[0]
    temphosts_dict = dict(cmd_group=dict(hosts=[]))
    for host_obj in host_set:
        host_ip = host_obj.ip
        print(currentThread().getName(), host_obj.ip)
        host_login_users_set = host_obj.login_user.all()
        password = ""
        for host_login_user in host_login_users_set:
            if host_login_user.name == "root":
                password = decrypt_p(host_login_user.password)
        host_dict = dict(ip=host_obj.ip, port=host_obj.port, username="root", password=password)
        temphosts_dict["cmd_group"]["hosts"].append(host_dict)
        #     上面的循环是为了拼凑成下面的形式
        # temphosts_dict = {
        #     "cmd_group": {
        #         "hosts": [{"ip": "10.0.0.62", "port": "22", "username": "root", "password": "123456"},
        #                   {"ip": "10.0.0.61", "port": "22", "username": "root", "password": "123456"}],
        #         "group_vars": {"var1": "ansible"}
        #     },
        #     # "Group2": {}
        # }
        cmd_path = os.path.join(BASE_DIR, "shell_script/get_host_info.sh")
        cmd = "sh %s" % cmd_path
        tasks = [dict(action=dict(module="shell", args=cmd, warn=False))]
        hosts = host_ip
        ar = AdhocRunner(temphosts_dict)
        ar.run_adhoc(hosts, tasks)
        failed = ar.get_adhoc_result().get("failed")
        ok = ar.get_adhoc_result().get("ok")
        unreachable = ar.get_adhoc_result().get("unreachable")
        task_id = host_ip + "---" + str(random.randrange(1, 99999999999999999999999999999999999))
        if failed:
            result[host_ip] = failed.get(host_ip).get("stderr")
            # TaskResult.objects.create(task_id=task_id,result=result[host_ip], task_name="pool_get_host_info")
        if unreachable:
            result[host_ip] = unreachable.get(host_ip).get("msg")
            # TaskResult.objects.create(task_id=task_id, result=result[host_ip], task_name="pool_get_host_info")
        if ok:
            result[host_ip] = ok.get(host_ip).get("stdout")  # mem:1990,host_name:m01,disk:30865437,cpu:2
            res_list = result[host_ip].split(",")  # ['mem:1990', 'host_name:m01', 'disk:30865437', 'cpu:2']
            mem = res_list[0].split(":")[1]
            host_name = res_list[1].split(":")[1]
            disk = res_list[2].split(":")[1]
            cpu = res_list[3].split(":")[1]
            query_host_obj = Host.objects.filter(ip=host_ip, hostname=host_name, disk=disk, cpu=cpu, mem=mem).first()
            # print("------------------------*%s*-----------------------"% host_obj)
            if not query_host_obj:
                # 不存在，就说明有数据更新了，就Update

                Host.objects.filter(ip=host_ip).update(hostname=host_name, disk=disk, cpu=cpu, mem=mem)
        #         报错信息存到task_result表中
        TaskResult.objects.create(task_id=task_id, result=result[host_ip], task_name="pool_get_host_info")

# 在celery调用ansible的时候，不管是定时任务还是一部任务，都得不到返回结果
# 搜索之后，发现说是celery3.1以上的版本，不支持另起子线程，
# 有两种方法解决这个问题，就是关闭assert：
# 1.在celery 的worker启动窗口设置export PYTHONOPTIMIZE=1或打开celery这个参数-O OPTIMIZATION
# 2.注释掉python包multiprocessing下面process.py中102行，关闭assert
#
#  export PYTHONOPTIMIZE=1 && celery -A CMDB worker --loglevel=info
@shared_task(name="pool_get_host_info")
def pool_get_host_info():
    """
    这个设置定时任务，每晚上空闲时间执行
    采用多线程的方式，这里使用了线程池，MAX_POOL_SIZE是线程池的大小
    :return:
    """
    host_set = Host.objects.all()
    pool = ThreadPoolExecutor(MAX_POOL_SIZE)
    host_set_count = Host.objects.all().count()
    # host_list  = [[],[],[]]
    host_list = []
    if host_set_count < MAX_POOL_SIZE:
        host_list.append(host_set)
    else:
        # Quotients and remainders
        # 求商和余数
        quotients = host_set_count//MAX_POOL_SIZE
        # remainders = host_set_count%MAX_POOL_SIZE
        for i in range(MAX_POOL_SIZE):
            li = []
            if i == MAX_POOL_SIZE - 1:
                # 如果循环到最后，就把剩下的所有数据放在最后一个列表中
                # 这样写是LIMIT 1 OFFSET 1'
                # 如果[i*quotients:]是 LIMIT 21 OFFSET 1
                host_set = Host.objects.all()[i*quotients:host_set_count]
            else:
                # b'SELECT `asset_host`.`id`, `asset_host`.`ip`, `asset_host`.`port`, `asset_host`.`note`,
                # `asset_host`.`MAC`, `asset_host`.`hostname`, `asset_host`.`cpu`, `asset_host`.`disk`,
                # `asset_host`.`mem`, `asset_host`.`operate_person_id`, `asset_host`.`system_id`, `
                # asset_host`.`environment_id`, `asset_host`.`expire_date`, `asset_host`.`create_time`,
                # `asset_host`.`update_time` FROM `asset_host`  LIMIT 1 OFFSET 1'; args=()
                host_set = Host.objects.all()[i*quotients:(i+1)*quotients]
            li.append(host_set)
            host_list.append(li)
    # print("host_list--------------",host_list)
    # [[<QuerySet [<Host: 10.0.0.61>]>], [<QuerySet [<Host: 10.0.0.62>]>],
    # [<QuerySet [<Host: 10.0.0.6>, <Host: 10.0.0.63>]>]]
    for host_set_list in host_list:
        pool.submit(get_host_info_func, host_set_list)

    pool.shutdown(wait=True)


@shared_task(name="sync_host_info")
def sync_host_info_task(pk):
    host_set_list = []
    host_set_list.append(Host.objects.filter(id=pk))
    # host_set_list = [<QuerySet [<Host: 10.0.0.61>]>]
    get_host_info_func(host_set_list)





