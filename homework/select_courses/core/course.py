#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita


class Course(object):
    def __init__(self):
        self.course_name = None
        self.period = None
        self.price = None
        self.associate_school_name = None
        # 教授这个课程的可能有多个班级，因为人太多啦。哈哈
        self.associate_class_names = []

    def setter(self, course_name, period, price, associate_school_name):
        self.course_name = course_name
        self.period = period
        self.price = price
        self.associate_school_name = associate_school_name
        return self
