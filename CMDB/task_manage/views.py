from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from web.utils import get_label, return_show_data
from asset.models import *
from web.models import *
from django.core.cache import cache
from task_manage.utils import get_data_from_cache


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

        # print('从redis中查询数据')
        host_obj_set = get_data_from_cache("Host")
        print("host_obj_set-------------------------------", host_obj_set)
        # <QuerySet [<Host: 10.0.0.61>, <Host: 10.0.0.62>, <Host: 10.0.0.6>]>
        env_obj_set = get_data_from_cache("Environment")
        sys_obj_set = get_data_from_cache("System")
        data_page_info = return_show_data(request, host_obj_set)

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


def get_host_by_sys_or_env_id(request):

    system_id = request.GET.get('system_id')
    environment_id = request.GET.get('environment_id')
    # 不知道为啥，动态添加的option,当
    if system_id and environment_id.isnumeric():
        host_list = list(Host.objects.filter(system_id=system_id, environment_id=environment_id).values("id", "ip"))
    elif not system_id and environment_id:
        host_list = list(Host.objects.filter(environment_id=environment_id).values("id", "ip"))
    elif system_id and not environment_id.isnumeric():
        host_list = list(Host.objects.filter(system_id=system_id).values("id", "ip"))
    elif not system_id and not environment_id.isnumeric():
        host_list = list(Host.objects.all().values("id", "ip"))

    return JsonResponse(host_list, safe=False)