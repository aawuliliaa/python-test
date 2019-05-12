#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
from core.accounts import Account, AdminAccount, TeacherAccount, StudentAccount
from utils.print_log import print_info
from conf.settings import ADMIN_NAME, ADMIN_PASSWORD, SCHOOL_PATH
from core.db import DbHandler, SchoolDbHandler
from core.school import School
from core.classes import Class
from core.course import Course


class View:
    account = Account()

    def __init__(self):
        pass
    user_data = {
                 'is_authenticated': False,
                 'account_data': None,
                 }

    def login(self, user_type):
        exit_flag = True
        while exit_flag:
            if not self.user_data["is_authenticated"]:
                username = input("input your name:").strip()
                password = input("input password:").strip()
                account_data = self.account.getter(username, user_type)
                if account_data is not None and account_data.user_type == user_type:
                    if account_data.password == password and account_data.username == username:
                        print_info("login success!")
                        self.user_data["is_authenticated"] = True
                        self.user_data["account_data"] = account_data
                        return True
                    else:
                        print_info("username or password is not correct!", "error")
                else:
                    print_info("your user_type is not %s" % user_type, "error")
            else:
                return self.user_data

    def log_out(self):
        """
        可用于老师登录，学生登录，管理员登录之后的退出登录，进入初始页面的操作。
        :return:
        """
        if self.user_data["is_authenticated"]:
            username = self.user_data["account_data"].username
            self.user_data = {
                "is_authenticated": False,
                "account_data": None
            }
            print_info("%s logout successful!" % username)

class AdminView(View):
    user_data = {
                 'is_authenticated': False,
                 'account_data': None,
                 }
    admin_account = AdminAccount()
    school_obj = School()
    class_obj = Class()
    course_obj = Course()
    teacher_obj = TeacherAccount()
    school_data = {'school': None,
                   'course': {},
                   'class': {},
                   'teacher': {},
                   'student': {}
                   }

    def __init__(self):
        self.create_admin_account()

    def login(self, user_type):
        """
        装饰器调用方法，必须先登录才能进行操作
        :param user_type:
        :return:
        """
        if super(AdminView, self).login(user_type):
            return True
        else:
            return False

    def create_admin_account(self):
        # 第一次登录，就创建管理员账号
        admin_account_obj = self.admin_account.setter(ADMIN_NAME, ADMIN_PASSWORD, "admin")
        if admin_account_obj:
            # 设置成功，说明admin是第一次登录，需要保存到文件中
            #
            db_handler_obj = DbHandler("admin", "admin", admin_account_obj)
            db_handler_obj.save_to_db()

    def create_school(self):
        """
        新建学校，保存到文件中
        :return:
        """
        exit_flag = True
        while exit_flag:
            school_name = input("please input school name:").strip()
            school_country = input("please input school country:").strip()
            school_city = input("please input school city:").strip()
            if school_name and school_country and school_city:

                school_obj = self.school_obj.setter(school_name, school_country, school_city)
                self.school_data["school"] = school_obj
                school_db_handler_obj = SchoolDbHandler(school_name, self.school_data)
                school_db_handler_obj.save_to_db()
                print_info("you have add this school to the file successful!")
                exit_flag = False
            else:
                print_info("your input is illegal", "error")
                exit_flag = False

    def create_class(self):
        """
        通过学校创建班级， 班级关联课程、讲师
        :return:
        """
        exit_flag = True
        while exit_flag:
            class_name = input("please input class name:").strip()
            associate_school_name = input("please input associate school name:").strip()
            associate_course_name = input("please input associate course name:").strip()
            associate_teacher_name = input("please input associate teacher name:").strip()
            school_path = "%s/%s" % (SCHOOL_PATH, associate_school_name)
            if os.path.exists(school_path):

                school_data = self.school_obj.getter(associate_school_name, None)
                # print_info(school_data)
                if associate_course_name not in school_data["course"]:
                    print_info("course %s is not exist! you can create it!" % associate_course_name, "error")
                    exit_flag = False
                elif associate_teacher_name not in school_data["teacher"]:
                    print_info("teacher %s is not exist! you can create it!" % associate_teacher_name, "error")
                    exit_flag = False
                else:
                    self.class_obj = self.class_obj.setter(class_name, associate_course_name,
                                                           associate_school_name, associate_teacher_name)
                    school_data["class"][class_name] = self.class_obj
                    school_db_handler_obj = SchoolDbHandler(associate_school_name, school_data)
                    school_db_handler_obj.save_to_db()
                    print_info("you have add this class to the school file successful!")
                    exit_flag = False
            else:
                print_info("this school is not exist!you can create it!", "error")
                exit_flag = False

    def create_course(self):
        """
        课程包含，周期，价格，通过学校创建课程
        :return:
        """
        exit_flag = True
        while exit_flag:
            course_name = input("please input course name:").strip()
            period = input("please input period[month]:").strip()
            price = input("please input price:").strip()
            associate_school_name = input("please input associate school name:").strip()
            school_path = "%s/%s" % (SCHOOL_PATH, associate_school_name)
            if os.path.exists(school_path):
                if period.isdigit() and price.isdigit():
                    school_data = self.school_obj.getter(associate_school_name, None)
                    self.course_obj = self.course_obj.setter(course_name, period, price, associate_school_name)
                    school_data["course"][course_name] = self.course_obj
                    school_db_handler_obj = SchoolDbHandler(associate_school_name, school_data)
                    school_db_handler_obj.save_to_db()
                    print_info("you have add this course to the school file successful!")
                    exit_flag = False
                else:
                    print_info("price and period must be a number!", "error")
                    exit_flag = False
            else:
                print_info("this school is not exist!you can create it!", "error")
                exit_flag = False

    def create_teacher(self):
        """
        创建讲师角色时要关联学校
        :return:
        """
        exit_flag = True
        while exit_flag:
            teacher_name = input("please input teacher name:").strip()
            teacher_password = input("please input teacher password:").strip()
            associate_school_name = input("please input associate school name:").strip()
            school_path = "%s/%s" % (SCHOOL_PATH, associate_school_name)
            if os.path.exists(school_path):
                school_data = self.school_obj.getter(associate_school_name, None)
                self.teacher_obj = self.teacher_obj.teacher_setter(teacher_name, teacher_password,
                                                           "teacher", associate_school_name)
                if self.teacher_obj:
                    school_data["teacher"][teacher_name] = self.teacher_obj
                    school_db_handler_obj = SchoolDbHandler(associate_school_name, school_data)
                    school_db_handler_obj.save_to_db()
                    db_handler_obj = DbHandler(teacher_name, "teacher", self.teacher_obj)
                    db_handler_obj.save_to_db()
                    # print_info("you have create this teacher and add this teacher to the school file successful!")
                    exit_flag = False
                else:
                    # 为FALSE，说明老师已经存在了
                    print_info("teacher has already exist!", "error")
                    exit_flag = False
            else:
                print_info("this school is not exist!you can create it!", "error")
                exit_flag = False

    def show_school_info(self):
        exit_flag = True
        while exit_flag:
            school_info = ""
            school_name = input("please input school name you want to show:").strip()
            school_path = "%s/%s" % (SCHOOL_PATH, school_name)
            if os.path.exists(school_path):
                school_data = self.school_obj.getter(school_name, None)
                for class_name in school_data["class"]:
                    school_info += "class_name:"
                    school_info += class_name
                    school_info += "  associate_course_name:"
                    school_info += school_data["class"][class_name].associate_course_name
                    school_info += "  associate_teacher_name:"
                    school_info += school_data["class"][class_name].associate_teacher_name
                    school_info += "\n"
                for course_name in school_data["course"]:
                    school_info += "course_name:"
                    school_info += course_name
                    school_info += "  period:"
                    school_info += school_data["course"][course_name].period
                    school_info += "  rice:"
                    school_info += school_data["course"][course_name].price
                    school_info += "\n"
                for teacher_name in school_data["teacher"]:
                    school_info += "teacher_name:"
                    school_info += teacher_name
                    school_info += "\n"
                for student_name in school_data["student"]:
                    school_info += "student_name:"
                    school_info += student_name
                    school_info += "\n"
                print_info(school_info)
                exit_flag = False
            else:
                print_info("this school is not exist!you can create it!", "error")
                exit_flag = False


class StudentView(View):
    student_obj = StudentAccount()

    def register(self):
        """
        注册新的学生账户
        :return:
        """
        exit_flag = True
        while exit_flag:
            username = input("please input username:").strip()
            password = input("please input password:").strip()
            if username and password:
                student_obj = self.student_obj.setter(username, password, "student")
                if student_obj:
                    db_handler_obj = DbHandler(username, "student", student_obj)
                    db_handler_obj.save_to_db()
                    print_info("you have registered successful!")
                    exit_flag = False
                else:
                    print_info("this user has already exist!", "error")
                    exit_flag = False
            else:
                print_info("username or password can not be null!", "error")
                exit_flag = False
    def choose_course(self):
        input("please choose one school first!")


class TeacherView(View):
    pass