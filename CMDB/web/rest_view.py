from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from web import models

from web import rest_searializer


# ViewSets define the view behavior.
# 这种方式，get,post请求，是restframwork已经帮助我们封装好了
# 但是要想自定制,还需要我们自己继承APIview来书写，灵活性会更好
# https://www.cnblogs.com/GGGG-XXXX/articles/9675911.html有说明
class MyUserViewSet(viewsets.ModelViewSet):
    queryset = models.MyUser.objects.all()
    serializer_class = rest_searializer.MyUserSerializer


class PrivilegeViewSet(viewsets.ModelViewSet):
    queryset = models.Privilege.objects.all()
    serializer_class = rest_searializer.PrivilegeSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = rest_searializer.RoleSerializer


class RoleView(APIView):
    """
    CBV方式的API，访问方式http://10.0.0.61:8080/api/Role
    # 在这个页面可以发送post请求，数据格式是get请求中的一个字典
    参考博客
    # https://www.cnblogs.com/GGGG-XXXX/articles/9568816.html

    """

    def get(self, request):
        # 每次请求都会执行一次
        # print("--------------------")
        role_list = models.Role.objects.all()
        ret = rest_searializer.RoleSerializer(role_list, many=True)
        # RESTful规范的返回结果
        #
        # 　　ret = {
        #                 code: 1000,
        #                 data:{
        #                     id:1,
        #                     name:'小强',
        #                     depart_id:http://www.luffycity.com/api/v1/depart/8/
        #                 },
        #                  error:{}
        #             }
        return Response(ret.data)

    def post(self, request):
        # book_obj = request.data
        print(request.data)
        serializer = rest_searializer.RoleSerializer(data=request.data)
        if serializer.is_valid():
            # print(12341253)
            serializer.save()
            return Response(serializer.validated_data)
        else:
            # {
            #     "non_field_errors": [
            #         "The fields name, code, parent_menu_name, child_menu_name, url must make a unique set."
            #     ]
            # }
            return Response(serializer.errors)

    def patch(self, request):
        # 在页面上测试发送pathch请求，数据格式为
        # {
        # "id":106,
        # "role_info":{"note":"notenew"}
        # }
        print(request.data)
        role_id = request.data["id"]
        role_obj = models.Role.objects.filter(pk=role_id).first()
        # role_info={"name":"","code":""...}key为models.py中的字段
        role_info = request.data["role_info"]
        serializer = rest_searializer.RoleSerializer(role_obj, data=role_info, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            #  #     {
            #     #     "detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"
            #     # }
            return Response(serializer.errors)


    def delete(self, request,id):
        print("------------------id")
        query_set = models.Role.objects.filter(id=id).first()
        if query_set:
            query_set.delete()
            return Response("")
        else:
            return Response("删除的角色不存在")


def rest_post_test(request):
    """
    rest POST请求测试,FBV方式
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "rest_post_test.html")
    else:
        data = json.loads(request.POST.get("data"))

        # many=True创建多条[{},{}]前端传过来的数据列表中方字典
        rest_obj = rest_searializer.RoleSerializer(data=data)
        if rest_obj.is_valid():
            rest_obj.save()

        return render(request, "rest_post_test.html", {"errors": rest_obj.errors, "data": rest_obj.data})

# python3.6中urllib模块的使用，get和post方法
# import urllib
# req = urllib.request.Request("http://10.0.0.61:8080/api/Role")
# page = urllib.request.urlopen(req).read()
# page = page.decode('utf-8')
# print("wwwwwwwwwwwwwwwwwwwww", type(page))  # <class 'str'>
# print("================",type(json.loads(page)))  # <class 'list'>
#
#
# # coding:utf-8
# from urllib import request
# from urllib import parse
# url = "http://10.1.2.151/ctower-mall-c/sys/login/login.do"
# data = {"id":"wdb","pwd":"wdb"}
# params="?"
# for key in data:
#   params = params + key + "=" + data[key] + "&"
# print("Get方法参数："+params)
# headers = {
#   #heard部分直接通过chrome部分request header部分
#   'Accept':'application/json, text/plain, */*',
#   'Accept-Encoding':'gzip, deflate',
#   'Accept-Language':'zh-CN,zh;q=0.8',
#   'Connection':'keep-alive',
#   'Content-Length':'14', #get方式提交的数据长度，如果是post方式，转成get方式：【id=wdb&pwd=wdb】
#   'Content-Type':'application/x-www-form-urlencoded',
#   'Referer':'http://10.1.2.151/',
#   'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
# }
# data = parse.urlencode(data).encode('utf-8')
# req = request.Request(url, headers=headers, data=data) #POST方法
# #req = request.Request(url+params) # GET方法
# page = urllib.request.urlopen(req).read()
# page = page.decode('utf-8')
# print(page)