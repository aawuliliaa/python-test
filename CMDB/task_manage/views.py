from django.views.generic import View
from django.shortcuts import render
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