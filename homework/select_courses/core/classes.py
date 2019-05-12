#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
class Class(object):
    def __init__(self):
        self.class_name = None
        # 对于专业的培训机构，应该是一个班级只教一种课程
        self.associate_course_name = None
        self.associate_school_name = None
        # 创建班级的时候，分配了老师
        self.associate_teacher_name = None
        # 用于列出该班级中有哪些学生
        self.students = []

    def setter(self,class_name, associate_course_name, associate_school_name, associate_teacher_name):
        self.class_name = class_name
        self.associate_course_name = associate_course_name
        self.associate_school_name = associate_school_name
        self.associate_teacher_name = associate_teacher_name
        return self

