from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
import paramiko
import os
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from web.utils import get_label, return_show_data
from asset.models import *
from web.models import *
from task_manage.utils import get_data_from_cache
from web.password_crypt import decrypt_p
from task_manage.my_ansible.run_adhoc import AdhocRunner

from CMDB import settings

# http://yshblog.com/blog/156
# 也可以把{}等使用json序列化为字符串，存入缓存中
class WebsshLogin(View):
    """
    webssh页面
    """
    def get(self, request, *args, **kwargs):

        left_label_dic = get_label(request)
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()
        # 从缓存获取
        # print('从redis中查询数据')
        host_obj_set = get_data_from_cache("Host")
        # print("host_obj_set-------------------------------", host_obj_set)
        # <QuerySet [<Host: 10.0.0.61>, <Host: 10.0.0.62>, <Host: 10.0.0.6>]>

        env_obj_set = get_data_from_cache("Environment")
        sys_obj_set = get_data_from_cache("System")
        web_ssh = settings.web_ssh
        web_port = settings.web_port
        # 上面内容是给前端渲染使用的

        # 搜索按钮点击时，

        if request.get_full_path().__contains__("selected_id"):
            # 由于前端会传三个字段的值，但是不知道哪个字段为空，哪个不为空，所以就拼接SQL
            # 拼接SQL就不需要判断多次啦，啦啦啦啦啦
            my_filter_condition = ""
            if len(request.GET.get("system_selected_id")) != 0:
                sys_id = request.GET.get("system_selected_id")
                # 这里一定注意，必须使用Q(),否则eval()报语法错误，因为=eval会进行赋值，但是eval不能进行赋值操作
                my_filter_condition += "Q(system_id=%s)" % sys_id
                if len(request.GET.get("environment_selected_id")) != 0 or \
                        len(request.GET.get("host_selected_id")) != 0:
                    my_filter_condition += " and "

            if len(request.GET.get("environment_selected_id")) != 0:
                env_id = request.GET.get("environment_selected_id")
                my_filter_condition += "Q(environment_id=%s)" % env_id
                if len(request.GET.get("host_selected_id")) != 0:
                    # 一定要加空格，否则语法错误
                    my_filter_condition += " and "
            if len(request.GET.get("host_selected_id")) != 0:
                host_id = request.GET.get("host_selected_id")
                my_filter_condition += "Q(id=%s)" % host_id

            if len(my_filter_condition) != 0:
                # 有查询条件
                list_host_obj_set = Host.objects.filter(eval(my_filter_condition))
            else:
                # 每个字段都为空
                list_host_obj_set = host_obj_set
        else:
            # 访问首页
            list_host_obj_set = host_obj_set

        data_page_info = return_show_data(request, list_host_obj_set)

        return render(request, 'task_manage/webssh_login.html', locals())


@login_required
def get_env_by_system_id(request):
    """
    系统，环境，主机三级联动
    系统选择器变了，环境选择器跟着变
    :param request:
    :return:
    """
    system_id = request.GET.get('system_id')
    result = {}
    if system_id:
        # 反向查询按表名小写，双下划线的方式查询
        # 在models.py中某个字段写了related_name,反向查询的时候就不能使用表名小写了
        env_list = list(Environment.objects.filter(system_environment__id=system_id).values("id", "name", "abs_name"))
        host_list = list(Host.objects.filter(system_id=system_id).values("id", "ip"))
    else:
        env_list = list(Environment.objects.all().values("id", "name", "abs_name"))
        host_list = list(Host.objects.all().values("id", "ip"))
    result["env_list"] = env_list
    result["host_list"] = host_list
    return JsonResponse(result, safe=False)


@login_required
def get_host_by_sys_or_env_id(request):
    """
    这个是环境选择器动了，主机选择器的数据动态变化
    :param request:
    :return:
    """
    system_id = request.GET.get('system_id')
    environment_id = request.GET.get('environment_id')
    host_list = []
    #
    if system_id and environment_id:
        host_list = list(Host.objects.filter(system_id=system_id, environment_id=environment_id).values("id", "ip"))
    elif not system_id and environment_id:
        host_list = list(Host.objects.filter(environment_id=environment_id).values("id", "ip"))
    elif system_id and not environment_id:
        host_list = list(Host.objects.filter(system_id=system_id).values("id", "ip"))
    elif not system_id and not environment_id:
        host_list = list(Host.objects.all().values("id", "ip"))
    return JsonResponse(host_list, safe=False)


@login_required
def get_host_login_user_info_by_id(request):
    host_login_user_id = request.POST.get("host_login_user_id")
    password = HostLoginUser.objects.filter(id=host_login_user_id).first().password
    dec_password = password
    return JsonResponse({"password": dec_password})


class RunCmd(View):
    """
    执行命令的页面
    """
    def get(self, request, *args, **kwargs):

        left_label_dic = get_label(request)
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()
        sys_obj_set = System.objects.all()
        return render(request, 'task_manage/run_cmd.html', locals())

    def post(self, request):
        # 获取前端传过来的数据
        # print(request.POST)
        # <QueryDict: {'book_authors_id_list[]': ['1', '3'], 'book_publish_id': ['2'],
        # 由于深度序列化，自动在key的后面加了个[]
        # 需要使用getlist方法获取数组值
        host_ip_list = request.POST.getlist("host_ip_list")
        # print("llllllllllllllllllllllllll",host_ip_list)
        cmd = request.POST.get("cmd")
        temphosts_dict = dict(cmd_group=dict(hosts=[]))
        # temphosts_dict["cmd_group"]["hosts"] = []
        for host_ip in host_ip_list:
            host_obj = Host.objects.filter(ip=host_ip).first()
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
        tasks = [dict(action=dict(module="shell", args=cmd, warn=False))]
        hosts = "cmd_group"
        ar = AdhocRunner(temphosts_dict)
        ar.run_adhoc(hosts, tasks)

        # changed = ar.get_adhoc_result().get("changed")
        # status = ar.get_adhoc_result().get("status")
        # skipped = ar.get_adhoc_result().get("skipped")
        failed = ar.get_adhoc_result().get("failed")
        ok = ar.get_adhoc_result().get("ok")
        unreachable = ar.get_adhoc_result().get("unreachable")
        result = {}
        for host_ip in host_ip_list:
            if failed:
                if host_ip in failed:
                    result[host_ip] = failed.get(host_ip).get("stderr")
            if unreachable:
                if host_ip in unreachable:
                    result[host_ip] = unreachable.get(host_ip).get("msg")
            if ok:
                if host_ip in ok:
                    result[host_ip] = ok.get(host_ip).get("stdout")

        return JsonResponse(result)


def taillog(request, hostname, port, username, password, private, tail_cmd):
    """
    执行 tail log 接口
    """
    channel_layer = get_channel_layer()
    user = request.user.name
    os.environ["".format(user)] = "true"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password:
        ssh.connect(hostname=hostname, port=port, username=username, password=decrypt_p(password))
    else:
        pkey = paramiko.RSAKey.from_private_key_file("{0}".format(private))
        ssh.connect(hostname=hostname, port=port, username=username, pkey=pkey)
    # cmd = "tail " + tail
    stdin, stdout, stderr = ssh.exec_command(tail_cmd, get_pty=True)
    for line in iter(stdout.readline, ""):
        if os.environ.get("".format(user)) == 'false':
            break
        result = {"status": 0, 'data': line}
        result_all = json.dumps(result)
        async_to_sync(channel_layer.group_send)(user, {"type": "user.message", 'text': result_all})


class TailLog(View):
    def get(self, request, *args, **kwargs):

        left_label_dic = get_label(request)
        # print(request.path)# /privilege/
        role_obj = Role.objects.filter(url=request.path).first()
        sys_obj_set = System.objects.all()
        host_obj_set = Host.objects.all()
        return render(request, 'task_manage/tail_log.html', locals())

    def post(self, request):
        ret = {'status': True, 'error': None, }
        ip = request.POST.get("ip")
        tail_cmd = request.POST.get("tail_cmd")
        host_obj = Host.objects.filter(ip=ip).first()
        password = ""
        private_key = ""
        for host_user_obj in host_obj.login_user.all():
            if host_user_obj.name == "root":
                password = host_user_obj.password
        try:
            taillog(request, ip, host_obj.port, "root", password,
                    private_key, tail_cmd)
        except Exception as e:
            ret['status'] = False
            ret['error'] = "错误{0}".format(e)

        return JsonResponse(ret)


class TailStop(View):
    """
       执行 tail_log  stop  命令
       """
    def post(self,request):
        ret = {'status': True, 'error': None, }
        name = request.user.name
        os.environ["".format(name)] = "false"
        return JsonResponse(ret)
