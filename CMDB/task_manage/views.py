from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
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
        # 从缓存获取
        # print('从redis中查询数据')
        host_obj_set = get_data_from_cache("Host")
        # print("host_obj_set-------------------------------", host_obj_set)
        # <QuerySet [<Host: 10.0.0.61>, <Host: 10.0.0.62>, <Host: 10.0.0.6>]>

        env_obj_set = get_data_from_cache("Environment")
        sys_obj_set = get_data_from_cache("System")
        # 搜索按钮点击时，
        # system_selected_id = request.GET.get("system_selected_id")
        # environment_selected_id = request.GET.get("environment_selected_id")

        # val = 0 if a == 0 else 2

        if request.get_full_path().__contains__("selected_id"):
            my_filter_condition = ""
            if len(request.GET.get("system_selected_id")) != 0:
                sys_id = request.GET.get("system_selected_id")
                # 这里一定注意，必须使用Q(),否则eval()报语法错误，因为=eval会进行赋值，但是eval不能进行赋值操作
                my_filter_condition += "Q(system_id=%s)" % sys_id
                if len(request.GET.get("environment_selected_id")) != 0 or len(request.GET.get("host_selected_id")) != 0:
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
                list_host_obj_set = Host.objects.filter(eval(my_filter_condition))
            else:
                list_host_obj_set = host_obj_set
        else:
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