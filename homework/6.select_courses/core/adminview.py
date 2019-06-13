#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import os
from core.views import View
from utils.print_log import print_info
from core.db import DbHandler, SchoolDbHandler
from core.accounts import AdminAccount, TeacherAccount
from conf.settings import SCHOOL_PATH
from core.classes import Class
from core.course import Course
from conf.settings import ADMIN_NAME, ADMIN_PASSWORD


class AdminView(View):

    admin_account = AdminAccount()

    class_obj = Class()
    course_obj = Course()
    teacher_obj = TeacherAccount()
    # 学校的时候使用
    school_data = {'school': None,
                   'course': {},
                   'class': {},
                   'teacher': {},
                   'student': {}
                   }

    def __init__(self):
        # 要使用父类中user_data
        super(AdminView,self).__init__()
        # 运行程序就会默认创建一个管理员账户
        self.create_admin_account()

    def create_admin_account(self):
        """
        第一次登录，就创建管理员账号
        :return:
        """
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
        """
        展示学校信息
        :return:
        """
        exit_flag = True
        while exit_flag:
            school_info = ""
            school_name = input("please input school name you want to show:").strip()
            school_path = "%s/%s" % (SCHOOL_PATH, school_name)
            if os.path.exists(school_path) and school_name:
                school_data = self.school_obj.getter(school_name, None)
                school_info += "class:\n"
                for class_name in school_data["class"]:
                    school_info += "class_name:%s" % class_name
                    school_info += "  associate_course_name:%s" % \
                                   school_data["class"][class_name].associate_course_name
                    school_info += "  associate_teacher_name:%s" % \
                                   school_data["class"][class_name].associate_teacher_name
                    school_info += "\n"
                school_info += "course:\n"
                for course_name in school_data["course"]:
                    school_info += "course_name:%s" % course_name
                    school_info += "  period:%s" % school_data["course"][course_name].period
                    school_info += "  rice:%s" % school_data["course"][course_name].price
                    school_info += "  associate_class_names:%s" % \
                                   str(school_data["course"][course_name].associate_class_names)
                    school_info += "\n"
                school_info += "teacher:\n"
                for teacher_name in school_data["teacher"]:

                    school_info += "teacher_name:%s" % teacher_name
                    school_info += " classes managed: %s" % str(school_data["teacher"][teacher_name].classes)
                    school_info += "\n"
                school_info += "student:\n"
                for student_name in school_data["student"]:
                    school_info += "student_name:%s" % student_name
                    school_info += "\n"
                print_info(school_info)
                exit_flag = False
            else:
                print_info("this school is not exist!you can create it!", "error")
                exit_flag = False
