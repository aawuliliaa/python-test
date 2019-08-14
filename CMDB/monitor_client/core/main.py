#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

import os
import pymysql
import time
from monitor_client.core.utils import get_ip,get_conn,get_table_name
from monitor_client import settings
from concurrent.futures import ThreadPoolExecutor
from threading import currentThread


class ReportData(object):
    """
    汇报数据类
    """
    def __init__(self):
        self.ip = get_ip('eth0')
        self.last_report_data_time_dic = {}
        self.conn = get_conn()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def pool_report_data_func(self, monitor_item_data_row):
        print("1111111111111111", currentThread().getName())
        # 监控脚本的内容
        monitor_script = monitor_item_data_row.get("monitor_script")
        # 监控项的名称
        name = monitor_item_data_row.get("name")
        # 报警表达式"load1<12 and load2<10"
        warn_expression = monitor_item_data_row.get("warn_expression")
        # 该监控项对应的表名
        monitor_item_table_name = get_table_name(name)
        # 脚本名称
        monitor_script_file_name = monitor_item_table_name + ".sh"
        if monitor_script is None:
            monitor_script = ""
        #     脚本的绝对路径
        script_asb_path = os.path.join(settings.TMP_DIR, monitor_script_file_name)
        # 脚本的内容写入文件中
        fw = open(file=script_asb_path, mode="w", encoding="utf-8")
        fw.write(monitor_script)
        # 千万别忘记close
        fw.close()
        os.popen("dos2unix %s" % script_asb_path)
        data = os.popen("sh %s" % script_asb_path).read()
        # 处理是否进行报警,注意，这里报错不会输出到控制台，debug一下就会看到。。因为是在线程池中，报错被捕获了
        data_list = data.split("_")  # ['load1:10', 'load2:23', 'load3:34']

        # str = "load1<12 and load2<10"
        # eval()有返回值，exec没有返回值
        for li in data_list:
            li = "=".join(li.split(":"))
            exec(li)
        # print("========",warn_expression)
        if warn_expression is not None:
            warn_or_not = eval(warn_expression)
        else:
            warn_or_not = False

        print("=================是否告警",warn_or_not)
        if warn_or_not is True:
            # 把数据添加到告警表中，dashbord显示告警信息
            warn_insert_sql = 'insert into monitor_warntable (get_data_time,name,warn_expression,ip, data) VALUES(NOW(),"{name}","{warn_expression}", "{ip}","{data}")'. \
                format(name=name, ip=self.ip, data=data, warn_expression=warn_expression,)  # 加个引号即可
            self.cursor.execute(warn_insert_sql)
            self.conn.commit()
        # 不能用防止sql注入的方式插入数据了，测试发现，
        # 表名是变量就会报语法错误''monitor_item_disk_75688b0220'，多了个引号，算了，就用这种方法把
        insert_sql = 'insert into {tabel_name} (get_data_time, ip, data, warn) VALUES(NOW(),"{ip}","{data}","{warn}")'. \
            format(tabel_name=monitor_item_table_name, ip=self.ip, data=data, warn=warn_or_not)  # 加个引号即可
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def report_data(self):
        """
        汇报数据
        :return:
        """
        # pymysql.err.InterfaceError: (0, '')
        # 这里如果连接pymysql，不关闭，就会自动断开连接，就会报上面的错
        # 下面几行是断开连接，就从新建立连接
        try:
            self.conn.ping()
        except:
            self.conn
        sql = """
        SELECT
            *
        FROM
            monitor_monitoritem
        WHERE
            id IN (
                SELECT DISTINCT
                    monitoritem_id
                FROM
                    monitor_template_monitor_item
                WHERE
                    template_id IN (
                        SELECT
                            template_id
                        FROM
                            monitor_template_host
                        WHERE
                            host_id = (
                                SELECT
                                    id
                                FROM
                                    asset_host
                                WHERE
                                    ip = "%s"
                            )
                    )
            )
        """ % self.ip

        self.cursor.execute(sql)
        monitor_item_data_rows = self.cursor.fetchall()
        # {'id': 9, 'name': 'disk', 'note': 'disk', 'monitor_script': 'df -h\r\nls', 'warn_expression': '',
        # 'time_interval': '', 'warn_type': 'email', 'create_time': datetime.datetime(2019, 8, 9, 7, 6, 56, 195393),
        # 'update_time': datetime.datetime(2019, 8, 9, 7, 6, 56, 195449)}

        # {'id': 10, 'name': 'mem', 'note': 'mem', 'monitor_script': 'mem', 'warn_expression': None,
        # 'time_interval': None,
        # 'warn_type': 'email', 'create_time': datetime.datetime(2019, 8, 9, 7, 16, 45, 991068),
        # 'update_time': datetime.datetime(2019, 8, 9, 7, 16, 45, 991102)}

        pool = ThreadPoolExecutor(settings.MY_THREAD_POOL_SIZE)
        for monitor_item_data_row in monitor_item_data_rows:

            time_interval = monitor_item_data_row.get("time_interval")
            name = monitor_item_data_row.get("name")
            if name not in self.last_report_data_time_dic:
                self.last_report_data_time_dic[name] = 0
            if time.time() - self.last_report_data_time_dic.get(name) > int(time_interval):
                pool.submit(self.pool_report_data_func, monitor_item_data_row)
                # 各自的上次汇报时间存放各自的，互不影响。。不能设置一个变量
                self.last_report_data_time_dic[name] = time.time()
                # 等所有的进程任务完成了，再继续主进程的代码
        pool.shutdown(wait=True)


if __name__ == '__main__':

    obj = ReportData()
    while True:
        obj.report_data()
        time.sleep(1)