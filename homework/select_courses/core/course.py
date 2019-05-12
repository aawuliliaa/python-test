#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita


class Course(object):
    def __init__(self):
        self.course_name = None
        self.period = None
        self.price = None
        self.associate_school_name = None

    def setter(self, course_name, period, price, associate_school_name):
        self.course_name = course_name
        self.period = period
        self.price = price
        self.associate_school_name = associate_school_name
        return self
