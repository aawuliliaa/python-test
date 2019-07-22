from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from web import models

from web import rest_searializer
from web import rest_auth

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
    由于添加了rest认证，所以访问的时候需要
    http://10.0.0.61:8080/api/Role?email=admin@qq.com&password=123
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


class TestAuthView(APIView):
    """
    rest POST请求测试,FBV方式
    :param request:
    :return:
    """
    # authentication_classes = [rest_auth.MyApiAuth, ]

    def get(self, request, *args, **kwargs):
        # http://10.0.0.61:8080/api/rest_post_test/?email=admin@qq.com&password=123
        # 这样请求才会出现页面
        # print(request.user)  # admin
        # print(request.auth.users_role.all())
        return render(request, "rest_post_test.html")

    def post(self, request):
        # http://10.0.0.61:8080/api/rest_post_test/?email=admin@qq.com&password=123
        # post请求的时候，请求路径要是上面的设置
        data = json.loads(request.POST.get("data"))
        # print("qqqqqqqqqqqqqqqqqqqqqqq", data)
        # many=True创建多条[{},{}]前端传过来的数据列表中方字典
        rest_obj = rest_searializer.PrivilegeSerializer(data=data)
        if rest_obj.is_valid():
            rest_obj.save()

        return render(request, "rest_post_test.html", {"errors": rest_obj.errors, "data": rest_obj.data})


# 1.python3.6中urllib模块的使用，get
# from  urllib import request
# import json
# req = request.Request("http://10.0.0.61:8080/api/Role?email=admin@qq.com&password=123")
# page = request.urlopen(req).read()
# page = page.decode('utf-8')
# print("wwwwwwwwwwwwwwwwwwwww", type(page))  # <class 'str'>
# print("================",type(json.loads(page)))  # <class 'list'>

# 2.post请求，不是自己定义的get.post
# from  urllib import request
# from  urllib import parse
#
# data = {
#     "name": "sd搜索s",
#     "note": "ss"
# }
# url = "http://10.0.0.61:8080/api/Privileges/?email=admin@qq.com&password=123"
# # 不加后面的用户名和密码报urllib.error.HTTPError: HTTP Error 403: Forbidden
# print(url)
# data = parse.urlencode(data).encode('utf-8')
# req = request.Request(url, data=data) #POST方法
#
# # print("rrrrrrrrrrrrrrrrr",req.data.decode("utf-8"))
# page = request.urlopen(req).read()
# # 如果数据插入报错，例如数据已经存在，或主键已经存在，会报urllib.error.HTTPError: HTTP Error 400: Bad Request
# page = page.decode('utf-8')
# print(page)
# # {"id":17,"name":"sd搜索s","note":"ss",
# "create_time":"2019-07-22T08:08:38.056705Z","update_time":"2019-07-22T08:08:38.056739Z"}
#

# 3.post请求，自定义的view
# from  urllib import request
# from  urllib import parse
#
# data = {
#         "id": 3,
#         "users": [
#             {
#                 "id": 2,
#                 "name": "lili"
#             },
#             {
#                 "id": 37,
#                 "name": "cc"
#             }
#         ],
#         "name": "运维",
#         "code": "operator",
#         "parent_menu_name": "资产信息",
#         "child_menu_name": "系统信息",
#         "url": "/system/",
#         "note": "系统信息"
#
#
#     }
# url = "http://10.0.0.61:8080/api/Role/?email=admin@qq.com&password=123"
# # 不加后面的用户名和密码报urllib.error.HTTPError: HTTP Error 403: Forbidden
# print(url)
# data = parse.urlencode(data).encode('utf-8')
# req = request.Request(url, data=data) #POST方法
#
# # print("rrrrrrrrrrrrrrrrr",req.data.decode("utf-8"))
# page = request.urlopen(req).read()
# # 如果数据插入报错，
# # 报错信息
# # {"non_field_errors":["The fields name, code, parent_menu_name, child_menu_name, url must make a unique set."]}
# page = page.decode('utf-8')
# print(page)

