#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

from core.views import StudentView, TeacherView, AdminView
from utils.print_log import print_info
teacher_view = TeacherView()
student_view = StudentView()
admin_view = AdminView()


def login_required(func):
    def inner(*args, **kwargs):
        if isinstance(args[0], TeacherView):
            if args[0].login("teacher"):
                func(*args, **kwargs)
        elif isinstance(args[0], StudentView):
            if args[0].login("student"):
                func(*args, **kwargs)
        elif isinstance(args[0], AdminView):
            if args[0].login("admin"):
                func(*args, **kwargs)
    return inner


def interactive(menu, menu_list):
    exit_flag = True
    while exit_flag:
        print_info(menu)
        your_choice = input("input your choice:").strip()
        if your_choice in menu_list:
            eval(menu_list[your_choice])
        else:
            print_info("your input is illegal!", "error")


def homepage():
    menu = """
    =============欢迎进入选课系统===============
    
                    1.学生登录
                    2.老师登录
                    3.管理员登录
                    4.退出程序
    
    ============================================
    """
    # 这里只能把函数写成字符串了，否则一定义列表，就执行了装饰器，就让登陆了，效果就不一样了
    # 后面使用eval()来进行解析
    menu_list = {
        "1": "student_login(student_view)",
        "2": "",
        "3": "admin_login(admin_view)",
        "4": "system_exit"
    }
    interactive(menu, menu_list)


def system_exit():
    """
    退出程序
    :return:
    """
    exit("thank you for coming this system,bye!")


@login_required
def admin_login(obj):
    """
    管理视图，创建讲师， 创建班级，创建课程
    :param obj:
    :return:
    """

    menu = """
    ================欢迎管理员登录===============
    
                    1.创建学校
                    2.创建班级
                    3.创建课程
                    4.创建老师
                    5.查看学校信息
                    6.退出
    
    =============================================
    """
    menu_list = {
        "1": "create_school(admin_view)",
        "2": "create_class(admin_view)",
        "3": "create_course(admin_view)",
        "4": "create_teacher(admin_view)",
        "5": "show_school_info(admin_view)",
        "6": "log_out(admin_view)"
    }
    interactive(menu, menu_list)


def create_school(obj):
    obj.create_school()


def create_class(obj):
    obj.create_class()


def create_course(obj):
    obj.create_course()


def create_teacher(obj):
    obj.create_teacher()


def show_school_info(obj):
    obj.show_school_info()


def student_login(obj):
    """
    学员视图， 可以注册， 交学费， 选择班级, 显示学员的选课信息
    :param obj:
    :return:
    """
    menu = """
    ===============欢迎进学员登录===============

                   1. 注册账号
                   2. 选择课程并付费
                   3. 选择班级
                   4. 展示学员信息
                   5. 退出
               
    ==============================================
    """
    menu_list = {
        "1": "register(student_view)",
        "2": "choose_course(student_view)",
        "3": "choose_class(student_view)",
        "4": "show_student_info(student_view)",
        "5": "logout(student_view)"
    }
    interactive(menu,menu_list)

def register(obj):
    obj.register()

@login_required
def choose_course(obj):
    obj.choose_course()
def log_out(obj):
    obj.log_out()
    homepage()
def run():
    homepage()
