#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
from core.views import View
from utils.print_log import print_info
from core.db import DbHandler, SchoolDbHandler
from core.accounts import StudentAccount
from conf.settings import SCHOOL_PATH


class StudentView(View):
    student_obj = StudentAccount()

    def __init__(self):
        # 要使用父类中user_data，这里主要是登录，退出时使用
        super(StudentView, self).__init__()

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
