# import pymysql
# import datetime
# import time
# def insert(id,io):
#
#     conn = pymysql.connect(user = "root", passwd = "123", host = "10.0.0.61", db = "test")
#     cur = conn.cursor()
#     sql = "insert into thred values ('%s','%s');"
#     cur.execute(sql%(io,int(id)))
#     cur.close()
#     conn.commit()
#
#
# if __name__ == "__main__":
#     import threading
#     t = threading.Thread(target=insert,args=(2,'in',))
#     t.start()
#     t = threading.Thread(target=insert,args=(3,'out',))
#     t.start()
#     t.join()




#coding *.* coding: utf-8 *.*
import pymysql
import time
# conn = MySQLdb.connect(
#     host = "192.2.4.166",
#     port = 3306,
#     user = "root",
#     passwd = 'qwe123',
#     db = 'python',
#     #如果遇到数据库中有中文，加这条
#     charset = "utf8",
# )
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

import os,time,random
def task(n):
    print('%s is runing' %os.getpid())

    return n**2

if __name__ == '__main__':

    executor=ThreadPoolExecutor(max_workers=3)

    # for i in range(11):
    #     future=executor.submit(task,i)

    executor.map(task,range(1,12)) #map取代了for+submit