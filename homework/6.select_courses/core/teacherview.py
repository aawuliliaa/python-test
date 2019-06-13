#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from core.views import View
from utils.print_log import print_info
from core.db import DbHandler, SchoolDbHandler


class TeacherView(View):
    def __init__(self):
        super(TeacherView, self).__init__()
        self.class_choice = None
        # 从学校的文件中，获取相关数据，后面用于修改和展示
        self.school_data = None

    def show_classes(self):
        """
        列出所管理的班级有哪些
        :return:
        """
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
        """
        选择班级
        :return:
        """
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
        """
        列出选择的班级中的学生
        :return:
        """
        exit_flag = True
        while exit_flag:
            if self.class_choice:
                student_info = ""
                if len(self.school_data["class"][self.class_choice].students) == 0:
                    print_info("there is not student in this class now")
                    exit_flag = False
                else:
                    for student_name in self.school_data["class"][self.class_choice].students:
                        student_info += student_name
                        student_info += "\n"
                    print_info(student_info)
                    exit_flag = False
            else:
                print_info("you must choose one class first!", "error")
                exit_flag = False

    def set_student_record(self):
        """
        设置学生成绩
        :return:
        """
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
