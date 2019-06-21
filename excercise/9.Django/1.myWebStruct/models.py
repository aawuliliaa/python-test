#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import pymysql


def get_data(user,password):
    conn = pymysql.connect(
        host="10.0.0.61",
        port=3306,
        user="root",
        password="123",
        database='db1'
    )
    cur = conn.cursor()

    sql = "select * from newuserinfo WHERE NAME ='%s' AND PASSWORD ='%s'" % (user, password)
    cur.execute(sql)
    return cur

