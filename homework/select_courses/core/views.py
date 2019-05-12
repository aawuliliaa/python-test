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
    school_obj = School()

    def __init__(self):
        pass
    # 登录的时候，会设置这个变量，后面获取用户的对象，都从这里获取
    # 保存登录状态
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
                        # 保存登录用户的对象到user_data中
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

    admin_account = AdminAccount()

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
        # 运行程序就会默认创建一个管理员账户
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
                school_path = "%s/%s" % (SCHOOL_PATH, school_name)
                if os.path.exists(school_path) and school_name:
                    print_info("this school has already exist!", "error")
                else:
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
            if os.path.exists(school_path) and associate_school_name:

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
                    # 课程对象也与班级联系起来，用于展示该教该课程的班级有哪些，可展示出来供用户选择
                    school_data["course"][associate_course_name].associate_class_names.append(class_name)
                    # 创建班级的时候，分配了老师，这里为了后面展示该老师管理哪些班级，把班级信息加入到老师对象中
                    teacher_obj = school_data["teacher"][associate_teacher_name]
                    teacher_obj.classes.append(class_name)
                    db_handler_obj = DbHandler(teacher_obj.username, "teacher", teacher_obj)
                    db_handler_obj.save_to_db()

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
            if os.path.exists(school_path) and associate_school_name:
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
            if os.path.exists(school_path) and associate_school_name:
                school_data = self.school_obj.getter(associate_school_name, None)
                self.teacher_obj = self.teacher_obj.teacher_setter(teacher_name, teacher_password,
                                                                   "teacher", associate_school_name)
                if self.teacher_obj:
                    school_data["teacher"][teacher_name] = self.teacher_obj
                    school_db_handler_obj = SchoolDbHandler(associate_school_name, school_data)
                    school_db_handler_obj.save_to_db()
                    db_handler_obj = DbHandler(teacher_name, "teacher", self.teacher_obj)
                    db_handler_obj.save_to_db()
                    print_info("you have create this teacher and add this teacher to the school file successful!")
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
            if os.path.exists(school_path) and school_name:
                school_data = self.school_obj.getter(school_name, None)
                for class_name in school_data["class"]:
                    school_info += "class_name:%s" % class_name
                    school_info += "  associate_course_name:%s" % \
                                   school_data["class"][class_name].associate_course_name
                    school_info += "  associate_teacher_name:%s" % \
                                   school_data["class"][class_name].associate_teacher_name
                    school_info += "\n"
                for course_name in school_data["course"]:
                    school_info += "course_name:%s" % course_name
                    school_info += "  period:%s" % school_data["course"][course_name].period
                    school_info += "  rice:%s" % school_data["course"][course_name].price
                    school_info += "  associate_class_names:%s" % \
                                   str(school_data["course"][course_name].associate_class_names)
                    school_info += "\n"
                for teacher_name in school_data["teacher"]:

                    school_info += "teacher_name:%s" % teacher_name
                    school_info += " classes managed: %s" % str(school_data["teacher"][teacher_name].classes)
                    school_info += "\n"
                for student_name in school_data["student"]:
                    school_info += "student_name:%s" % student_name
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
            username = input("please input new username:").strip()
            password = input("please input new password:").strip()
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
        exit_flag = True
        while exit_flag:
            course_info = "=====the course listed below is for your choose====\n"
            associate_school_name = input("please choose one school first!").strip()
            if os.path.exists("%s/%s" % (SCHOOL_PATH, associate_school_name)) and associate_school_name:
                school_data = self.school_obj.getter(associate_school_name, None)
                for course_name in school_data["course"]:

                    course_info += course_name
                    course_info += school_data["course"][course_name].price
                    course_info += "\n"
                # 列出该学校下可供选择的课程有哪些
                print_info(course_info)
                associate_course_name = input("please input course:").strip()
                associate_course_price = input("please input course price:").strip()
                if associate_course_name not in school_data["course"] or \
                        associate_course_price != school_data["course"][associate_course_name].price:
                    print_info("your input course name not exist or price is not right!", "error")
                    exit_flag = False
                else:
                    # 课程对象：course_name:python  period:6  rice:9000  associate_class_names:['python12']
                    # 列出在所选的课程下，有哪些班级供选择
                    course_obj = school_data["course"][associate_course_name]
                    class_info = "=====the class listed below is for your choose====\n"
                    for class_name in course_obj.associate_class_names:

                        class_info += class_name
                        class_info += "\n"
                    print_info(class_info)
                    associate_class_name = input("please input class name:").strip()
                    if associate_class_name not in course_obj.associate_class_names:
                        print_info("your input is illegal!", "error")
                        exit_flag = False
                    else:
                        # 老师自动分配
                        student_obj = self.user_data["account_data"]
                        student_obj.associate_course_name = associate_course_name
                        student_obj.associate_class_name = associate_class_name
                        student_obj.associate_school_name = associate_school_name
                        student_obj.associate_course_price = associate_course_price
                        school_data["student"][student_obj.username] = student_obj
                        # 学生选好了班级后，就把学生的名字加入班级对象下的students中，后面用于展示该班级中的学生
                        school_data["class"][associate_class_name].students.append(student_obj.username)
                        db_handler_obj = DbHandler(student_obj.username, "student", student_obj)
                        db_handler_obj.save_to_db()
                        school_db_handler_obj = SchoolDbHandler(associate_school_name, school_data)
                        school_db_handler_obj.save_to_db()
                        print_info("you have update user info to db file and school file!")
                        exit_flag = False
            else:
                print_info("this school not exist", "error")
                exit_flag = False

    def show_student_info(self):
        exit_flag = True
        while exit_flag:
            student_obj = self.user_data["account_data"]
            student_info = ""
            student_info += "username:%s \n" % student_obj.username
            if student_obj.associate_school_name:
                student_info += "associate_school_name:%s \n" % student_obj.associate_school_name
            if student_obj.associate_course_name:
                student_info += "associate_course_name:%s \n" % student_obj.associate_course_name
            if student_obj.associate_course_price:
                student_info += "associate_course_price:%s \n" % student_obj.associate_course_price
            if student_obj.associate_class_name:
                student_info += "associate_class_name:%s \n" % student_obj.associate_class_name
            if student_obj.record:
                student_info += "record:%s\n" % student_obj.record
            print_info(student_info)
            exit_flag = False


class TeacherView(View):
    def __init__(self):
        super(TeacherView,self).__init__()
        self.class_choice = None
        # 从学校的文件中，获取相关数据，后面用于修改和展示
        self.school_data = None

    def show_classes(self):
        exit_flag = True
        while exit_flag:
            teacher_obj = self.user_data["account_data"]
            class_info = ""
            for class_name in teacher_obj.classes:

                class_info += class_name
                class_info += "\n"
            print_info(class_info)
            exit_flag = False

    def choose_class(self):
        exit_flag = True
        while exit_flag:
            class_choice = input("please choose one class you want to manage:").strip()
            if class_choice not in self.user_data["account_data"].classes:
                print_info("your input class not exist!", "error")
                exit_flag = False
            else:
                self.class_choice = class_choice
                print_info("you have choose %s class successful!" % class_choice)
                teacher_obj = self.user_data["account_data"]
                associate_school_name = teacher_obj.associate_school_name
                school_data = self.school_obj.getter(associate_school_name, None)
                self.school_data = school_data
                exit_flag = False

    def list_student(self):
        exit_flag = True
        while exit_flag:
            if self.class_choice:
                student_info = ""

                for student_name in self.school_data["class"][self.class_choice].students:
                    student_info += student_name
                    student_info += "\n"
                print_info(student_info)
                exit_flag = False
            else:
                print_info("you must choose one class first!", "error")
                exit_flag = False

    def set_student_record(self):
        exit_flag = True
        while exit_flag:
            student_name = input("please input student name:").strip()
            student_record = input("please set record:").strip()
            if student_name not in self.school_data["student"]:
                print_info("the student not exist!", "error")
                exit_flag = False
            elif not student_record.isdigit():
                print_info("record can just be a number!", "error")
                exit_flag = False
            else:
                student_obj = self.school_data["student"][student_name]
                student_obj.record = student_record
                db_handler_obj = DbHandler(student_obj.username, "student", student_obj)
                db_handler_obj.save_to_db()
                school_db_handler_obj = SchoolDbHandler(student_obj.associate_school_name, self.school_data)
                school_db_handler_obj.save_to_db()
                print_info("set record successful!")
                exit_flag = False
