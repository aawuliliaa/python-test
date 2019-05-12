#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
class Class(object):
    def __init__(self):
        self.class_name = None
        self.associate_course_name = None
        self.associate_school_name = None
        self.associate_teacher_name = None

    def setter(self,class_name, associate_course_name, associate_school_name, associate_teacher_name):
        self.class_name = class_name
        self.associate_course_name = associate_course_name
        self.associate_school_name = associate_school_name
        self.associate_teacher_name = associate_teacher_name
        return self

