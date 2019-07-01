from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import auth
from django.core import serializers
from app.models import *
from app.page import my_page, set_page_session


def login(request):
    # 登录函数
    if request.method == "POST":
        res = {"user": None, "info": None}
        # 获取前端传过来的数据
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user_obj = User.objects.filter(username=user)
        # 用户存在
        if user_obj:
            # 验证用户名和密码是否正确
            auth_user_obj = auth.authenticate(username=user, password=pwd)
            if auth_user_obj:
                # 验证通过
                auth.login(request, auth_user_obj)

                res["user"] = user
                # 登录成功后，设置返回首页的url,由于多处使用，所以防在了session中
                request.session["back_url"] = "/index/"

            else:
                res["info"] = "密码错误！"

        else:
            # 用户不存在时
            res["info"] = "用户不存在！"
        #     这种方式可以传中文到前端
        return JsonResponse(res)

    return render(request, "login.html")


def register(request):
    # 注册函数
    if request.method == "POST":
        res = {"user": False, "info": None}
        # 获取前端传过来的用户名与密码
        user = request.POST.get("user").strip()
        pwd = request.POST.get("pwd").strip()
        # 验证前端传过来的数据
        if user == "" or pwd == "":
            res["info"] = "user or password can not be null!"
            return JsonResponse(res)
        # 到数据库中获取用户信息
        user_obj = User.objects.filter(username=user)

        # 如果该用户已经存在，返回信息，不存在，插入该用户信息到数据库
        if user_obj:
            res["info"] = "user already exist!"

            return JsonResponse(res)
        # 用户不存在，就创建该用户
        User.objects.create_user(username=user, password=pwd)
        # 创建成功
        res["user"] = user
        # 这种方式不能传中文，前端会解析报错
        return JsonResponse(res)
    # get请求时，跳转在login页面。
    # 这里不能加装饰器，加了之后，发现前端success后，接收的data是login.html，所以这里使用这种方式
    return render(request, "login.html")

# 需要auth.login()之后，才允许登录。auth.login会设置相关信息到session中
@login_required
def index(request):
    # 由于三个列表，是分别设置的分页操作，这里主要是让各自的分页互不影响。
    set_page_session(request)
    # 展示信息页面，这都是为了不让前端出现黄色的警告。。也可以直接写在前端的
    logout_url = "/logout/"
    add_book_url = "/add_book/"
    # 前端展示数据使用
    author_list = Author.objects.all()
    publish_list = Publish.objects.all()
    book_list = Book.objects.all()
    # 分页信息
    # 这里是为了让三个列表的分页操作互不影响而加的代码。
    # 由于我是把三个列表都展示在一个页面了，可能某个列表数据很多，某个列表数据很少，所以设置了三个单独的列表
    book_page_info = my_page(book_list, request.session.get("book_page"))
    author_page_info = my_page(author_list, request.session.get("author_page"))
    publish_page_info = my_page(publish_list, request.session.get("publish_page"))
    return render(request, "index.html", locals())


@login_required
def logout(request):
    # 退出登录，删除session,cookie信息
    auth.logout(request)
    return redirect("/login/")


@login_required
def add_author(request):
    # 添加作者信息
    # 这里没有做作者姓名唯一性限制，因为作者姓名是可以重复的
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        author_name = request.POST.get("author_name").strip()
        author_age = request.POST.get("author_age").strip()
        # 验证前端传过来的数据
        if author_name == "" or author_age == "":
            res["info"] = "作者名或年龄不能为空"
        elif not author_age.isnumeric():
            res["info"] = "年龄必须是数字"
        else:
            try:
                # 添加用户信息
                Author.objects.create(name=author_name, age=author_age)
                res["success"] = True
                res["info"] = "%s 作者添加成功" % author_name
            except Exception as e:
                print(e)
                res["info"] = "插入数据报错，请查看端日志！"
        return JsonResponse(res)


@login_required
def edit_author(request, author_id):
    # 编辑作者信息
    # 这是之前写的跳转页面方式使用的代码
    # author_id = int(author_id)
    # author_obj = Author.objects.get(id=author_id)
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        author_name = request.POST.get("author_name").strip()
        author_age = request.POST.get("author_age").strip()
        # 验证前端传过来的数据
        if author_name == "" or author_age == "":
            res["info"] = "作者名或年龄不能为空"
        elif not author_age.isnumeric():
            res["info"] = "年龄必须是数字"
        else:
            try:
                # 修改作者信息
                Author.objects.filter(id=author_id).update(name=author_name, age=author_age)
                res["success"] = True
                res["info"] = "%s 作者修改成功" % author_name
            except Exception as e:
                print(e)
                res["info"] = "更新数据报错，请查看端日志！"
        return JsonResponse(res)
    # return render(request, "author_edit.html", locals())


@login_required
def show_author(request, author_id):
    # 列出选择的作者出版了哪些书
    author_id = int(author_id)
    author_obj = Author.objects.get(id=author_id)
    author_book_list = Book.objects.filter(authors__id=author_id)

    return render(request, "author_book.html", locals())


@login_required
def del_author(request, author_id):
    # 删除作者信息
    Author.objects.get(id=author_id).delete()
    return redirect("/index/")


@login_required
def add_publish(request):
    # 插入出版社信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        publish_name = request.POST.get("publish_name").strip()
        publish_city = request.POST.get("publish_city").strip()
        publish_email = request.POST.get("publish_email").strip()
        # 验证前端传过来的数据
        if publish_name == "" or publish_city == "" or publish_email == "":
            res["info"] = "出版社名字-城市-邮箱不能为空哦！"
        elif not publish_email.__contains__("@"):
            res["info"] = "出版社邮箱格式错误！"
        elif Publish.objects.filter(name=publish_name, city=publish_city):
            res["info"] = "同样的城市中出版社只能有一个"
        else:
            # 插入数据可能报错
            try:
                Publish.objects.create(name=publish_name, city=publish_city, email=publish_email)
                res["success"] = True
                res["info"] = "%s 出版社添加成功" % publish_name
            except Exception as e:
                print(e)
                res["info"] = "插入数据报错，请查看端日志！"

        return JsonResponse(res)


@login_required
def edit_publish(request, publish_id):
    # 编辑出版社信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        publish_name = request.POST.get("publish_name").strip()
        publish_city = request.POST.get("publish_city").strip()
        publish_email = request.POST.get("publish_email").strip()
        # 验证前端传过来的数据
        if publish_name == "" or publish_city == "" or publish_email == "":
            res["info"] = "出版社名字-城市-邮箱不能为空哦！"
        elif not publish_email.__contains__("@"):
            res["info"] = "出版社邮箱格式错误！"
        elif Publish.objects.filter(name=publish_name, city=publish_city):
            res["info"] = "同样的城市中出版社只能有一个"
        else:
            # 插入数据可能报错
            try:
                Publish.objects.filter(id=publish_id).update(name=publish_name, city=publish_city, email=publish_email)
                res["success"] = True
                res["info"] = "%s 出版社编辑成功" % publish_name
            except Exception as e:
                print(e)
                res["info"] = "修改数据报错，请查看端日志！"

        return JsonResponse(res)
    
    # get请求时
    # publish_obj = Publish.objects.get(id=publish_id)
    #
    # return render(request, "publish_edit.html", locals())


@login_required
def show_publish(request, publish_id):
    # 展示出版社出版的书籍信息
    publish_obj = Publish.objects.get(id=publish_id)
    publish_book_list = Book.objects.filter(publish__id=publish_id)
    return render(request, "publish_book.html", locals())


@login_required
def del_publish(request, publish_id):
    # 删除出版社信息
    Publish.objects.get(id=publish_id).delete()
    return redirect("/index/")


@login_required
def add_book(request):
    # 添加书籍
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        # print(request.POST)
        # <QueryDict: {'book_authors_id_list[]': ['1', '3'], 'book_publish_id': ['2'],
        # 由于深度序列化，自动在key的后面加了个[]
        # 需要使用getlist方法获取数组值
        book_author_id_list = request.POST.getlist("book_authors_id_list")
        book_publish_id = request.POST.get("book_publish_id").strip()
        book_title = request.POST.get("book_title").strip()
        book_publish_date = request.POST.get("book_publishDate").strip()
        book_price = request.POST.get("book_price").strip()
        # 验证前端传过来的数据
        if len(book_author_id_list) == 0 or book_publish_id == "" \
                or book_title == "" or book_publish_date == "" or book_price == "":
            res["info"] = "添加的内容不能为空哦！"
        elif not book_price.replace(".", "").isnumeric():
            res["info"] = "价格只能是数字！"
        elif Book.objects.filter(title=book_title):
            res["info"] = "书名不能重复"
        else:
            # 插入数据可能报错
            try:
                book_obj = Book.objects.create(title=book_title, price=book_price,
                                               publishDate=book_publish_date, publish_id=book_publish_id)
                # print(book_author_id_list)  # ['2', '3']

                book_obj.authors.add(*book_author_id_list)
                res["success"] = True
                res["info"] = "%s 添加成功" % book_title
            except Exception as e:
                print(e)
                res["info"] = "插入数据报错，请查看端日志！"

        return JsonResponse(res)
    # get请求时，页面需要列出出版社和作者信息供用户选择
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()

    # 把queryset序列化
    json_author_list = serializers.serialize('json', author_list)
    json_publish_list = serializers.serialize('json', publish_list)
    
    # return render(request, "book_add.html", locals())
    return JsonResponse({"json_author_list": json_author_list, "json_publish_list": json_publish_list})


@login_required
def edit_book(request, book_id):
    book_obj = Book.objects.get(id=book_id)
    # 编辑书本信息
    if request.method == "POST":
        res = {"success": False, "info": None}
        # 获取前端传过来的数据
        # print(request.POST)
        # <QueryDict: {'book_authors_id_list[]': ['1', '3'], 'book_publish_id': ['2'],
        # 由于深度序列化，自动在key的后面加了个[]
        # 需要使用getlist方法获取数组值
        book_author_id_list = request.POST.getlist("book_authors_id_list")

        book_publish_id = request.POST.get("book_publish_id").strip()
        book_title = request.POST.get("book_title").strip()
        book_publish_date = request.POST.get("book_publishDate").strip()
        book_price = request.POST.get("book_price").strip()
        # 验证前端传过来的数据
        if book_author_id_list is None or book_publish_id == "" \
                or book_title == "" or book_publish_date == "" or book_price == "":
            res["info"] = "编辑的内容不能为空哦！"
        elif not book_price.replace(".", "").isnumeric():
            res["info"] = "价格只能是数字！"
        else:
            # 插入数据可能报错
            try:
                Book.objects.filter(id=book_id).update(title=book_title, price=book_price,
                                                       publishDate=book_publish_date, publish_id=book_publish_id)
                # print(book_author_id_list)  # ['2', '3']

                # edit_book_obj.authors.clear()
                # edit_book_obj.authors.add(*authors_id_list)

                book_obj.authors.set(book_author_id_list)
                res["success"] = True
                res["info"] = "%s 编辑成功" % book_title
            except Exception as e:
                print(e)
                res["info"] = "插入数据报错，请查看端日志！"

        return JsonResponse(res)
    
    # get请求时，页面需要列出出版社和作者信息供用户选择
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    
    # publish_str = ""
    # author_str = ""
    # for publish_obj in publish_list:
    #     if book_obj.publish.id == publish_obj.id:
    #         publish_str += "<option value = %s selected >%s </option>" % (publish_obj.id, publish_obj.name)
    #     else:
    #         publish_str += "<option value = %s  >%s </option>" % (publish_obj.id, publish_obj.name)
    #         
    # for author_obj in author_list:
    #     if author_obj in book_obj.authors.all():
    #         author_str += "<option value = %s selected >%s </option>" % (author_obj.id, author_obj.name)
    #     else:
    #         author_str += "<option value = %s  >%s </option>" % (author_obj.id, author_obj.name)
    #         弹出页面方式时的写法
    # return render(request, "book_edit.html", locals())
    # 弹出模态框时的写法
    # 把queryset序列化
    json_author_list = serializers.serialize('json', author_list)
    json_publish_list = serializers.serialize('json', publish_list)
    book_author_list = []
    for book_author_obj in book_obj.authors.all():
        book_author_list.append(book_author_obj.id)
    # 这里，由于需要通过book_obj.authors获取多个用户id，所以就在后端处理成字典，传到前端
    json_book_obj = {"publish_id": book_obj.publish.id, "author_id_list": book_author_list, 
                     "book_id": book_obj.id, "book_price": book_obj.price, "book_publishDate": book_obj.publishDate, 
                     "book_title": book_obj.title}
    return JsonResponse({"json_author_list": json_author_list, 
                         "json_publish_list": json_publish_list, "json_book_obj": json_book_obj})
    

@login_required
def del_book(request, book_id):
    # 删除书籍信息
    print(request)
    Book.objects.filter(id=book_id).delete()
    return redirect("/index/")
