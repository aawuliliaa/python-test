#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from tabulate import tabulate
import os
import uuid
import re
COLUMNS = ['staff_id', 'name', 'age', 'phone', 'dept', 'enrolled_date']
SOURCE_FILE = "staff_table.txt"
NEW_SOURCE_FILE = "new_staff_table.txt"


# 字典形式，便于数据的获取和查找，其中设置key为phone，是因为phone是唯一的
def load_db():
    # staff_db = {13764739091:{id:1,name:vita,age:27,phone:13764739091,dept:IT,enrolled_date:2017-03-04},13964739082:{}}
    all_staff_db = {}
    f = open(file=SOURCE_FILE, mode="r", encoding="utf-8")
    for line in f:
        # 后面有空行的时候回报错，预防空行的报错问题
        if len(line.strip()) > 0:
            staff_id, name, age, phone, dept, enrolled_date = line.split(",")
            all_staff_db[phone] = {"staff_id": staff_id, "name": name, "age": age, "phone": phone,
                                   "dept": dept, "enrolled_date": enrolled_date}
    return all_staff_db


# 修改后的数据保存到文件中
def save_db(new_staff_db):
    f = open(file=NEW_SOURCE_FILE, mode="w", encoding="utf-8")
    for phone, one_staff_info in new_staff_db.items():
        new_one_staff = []
        for column in COLUMNS:
            # 添加数据的时候，处理换行问题。否则数据就都添加到结尾了
            if column == "enrolled_date":
                if not one_staff_info[column].endswith("\n"):
                    one_staff_info[column] += "\n"
            new_one_staff.append(one_staff_info[column])

        # ",".join(["1","2"]) = 1,2,变成字符串，可以保存到文件中
        f.write(",".join(new_one_staff))
    f.close()
    # 先删除，再重命名。。这里已经尝试了，直接rename报错
    os.remove(SOURCE_FILE)
    os.rename(NEW_SOURCE_FILE, SOURCE_FILE)


# 输出提示信息
def print_info(info, log_type="info"):
    if log_type == "info":
        print("\033[32;1m %s \033[0m" % info)
    elif log_type == "error":
        print("\033[31;1m %s \033[0m" % info)


# where后的条件是'>',查找符合条件的数据
def gt_data(where_column, value, all_staff_db, gt_data_return):

    if value.isdigit():
        for phone in all_staff_db:
            if int(all_staff_db[phone][where_column]) > int(value):
                gt_data_return[phone] = all_staff_db[phone]
        return gt_data_return
    # 如果>后面不是数字
    print_info("the value after where condition '>' must bu a number", "error")


# where后的条件是'<',查找符合条件的数据
def lt_data(where_column, value, all_staff_db, lt_data_return):

    if value.isdigit():
        for phone in all_staff_db:
            if int(all_staff_db[phone][where_column]) < int(value):
                lt_data_return[phone] = all_staff_db[phone]
        return lt_data_return
    # 如果<后面不是数字
    print_info("the value after where condition '<' must be a number", "error")


# where后的条件是'=',查找符合条件的数据
def eq_data(where_column, value, all_staff_db, eq_data_return):

    for phone in all_staff_db:

        if all_staff_db[phone][where_column] == value:
            eq_data_return[phone] = all_staff_db[phone]
    return eq_data_return


# where后的条件是'like',查找符合条件的数据
def like_data(where_column, value, all_staff_db, eq_data_return):

    for phone in all_staff_db:
        if value in all_staff_db[phone][where_column]:
            eq_data_return[phone] = all_staff_db[phone]
    return eq_data_return


# 找出符合where条件的数据，然后进行增删改查
def where_condition_data(input_sql, all_staff_db):
    condition_list = {
        ">": gt_data,
        "<": lt_data,
        "=": eq_data,
        "like": like_data
    }
    # find age from staff_db where age = 3
    # where_condition age = 3
    where_condition = input_sql.split("where")[1].strip()
    # 这里作为参数传给函数，就不需要在每个函数中定义了
    return_data = {}
    for condition in condition_list:
        if condition in where_condition:
            where_column, value = where_condition.split(condition)
            # find * from table where dept = "IT"
            # 当查询语句含有双引号时，要去除双引号，value.strip(' "')意思是去除首和尾的空格和双引号
            # value = value.strip(' "'))
            if where_column.strip() in COLUMNS:
                # 查找符合where条件的数据
                where_data = condition_list[condition](where_column.strip(), value.strip(' "'),
                                                       all_staff_db, return_data)
                return where_data
            else:
                print_info("the column of where is not exist!", "error")
    else:
        # 如果where条件中不是>,<,=,就输出语法错误
        print_info("your input sql is illegal!", "error")


# 查找符合条件的数据
def find_condition(where_data, input_sql, all_staff_db):
    # find age from staff_db where age = 3
    # find age,name from staff_db where age = 3
    if "*" in input_sql:
        # ['id', 'name', 'age', 'phone', 'dept', 'enrolled_date']
        header = COLUMNS
    else:
        columns = input_sql.split()[1]
        header = columns.split(",")
    for column in header:
        # 验证列是否存在
        if column not in COLUMNS:
            print_info("find column %s is not exist" % column, "error")
            return None
    final_many_data = []

    for phone, one_staff_info in where_data.items():
        final_one_data = []
        for column in header:
            final_one_data.append(one_staff_info[column])
        # final_many_data = [['18', 'Jack Wang'], ['18', 'Eric Liu']]
        final_many_data.append(final_one_data)
    print(tabulate(final_many_data, headers=header, tablefmt="grid"))

    print_info("匹配到%s条数据!" % len(final_many_data))


# 删除数据库中的数据
def del_condition(where_data, input_sql, all_staff_db):
    for phone in where_data:
        del all_staff_db[phone]
    save_db(all_staff_db)
    print_info("匹配到%s条数据!" % len(where_data))


# 更新数据库
def update_condition(where_data, input_sql, all_staff_db):
    # update staff_table set dept="Market" where dept = "IT"
    # set_condition = 'dept="Market"'
    set_conditions = input_sql.split("where")[0].strip().split("set")[1].strip()
    # update staff_table set dept=Market,age="22" where dept = "Market" 可以给多列设值，也可以给值加引号
    for set_condition in set_conditions.split(","):
        set_column, set_value = set_condition.strip().split("=")
        set_column = set_column.strip()
        if set_column not in COLUMNS:
            print_info("update column %s is not exist" % set_column, "error")
            return None
        # update staff_table set dept=Market,age="22" where dept = "Market"
        set_value = set_value.strip(' "')
        if set_column == "phone":
            if set_value in all_staff_db:
                print_info("this phone number has already exist!", "error")
                return None
        for phone, one_staff_info in where_data.items():
            one_staff_info[set_column] = set_value
        # 新数据更新到all_staff_db中
            all_staff_db[phone] = one_staff_info

    save_db(all_staff_db)
    print_info("匹配到%s条数据!" % len(where_data))


# add staff_table Moon,18,13678789527,IT,2018-12-11
def add_condition(where_data, input_sql, all_staff_db):
    columns = input_sql.split()[2].strip()
    name, age, phone, dept, enrolled_date = columns.split(",")
    if phone in all_staff_db:
        print_info("this phone number has already exist!", "error")
        return None
    staff_id = str(uuid.uuid1())
    all_staff_db[phone] = {}
    all_staff_db[phone]["staff_id"] = staff_id
    all_staff_db[phone]["name"] = name
    all_staff_db[phone]["age"] = age
    all_staff_db[phone]["phone"] = phone
    all_staff_db[phone]["dept"] = dept
    all_staff_db[phone]["enrolled_date"] = enrolled_date

    save_db(all_staff_db)


# 验证输入的sql语句是否符合规则
def verify_sql(condition,input_sql):
    if condition == 'find':
        if re.match("find[ ]+[^ ]+[ ]+from[ ]+[^ ]+[ ]*", input_sql) is None:
            print_info("find sql example:find age,name from staff_table", "error")
            return False
    elif condition == 'update':
        if re.match("update[ ]+[^ ]+[ ]+set[ ]+.*[=].*[ ]+where.*", input_sql) is None:
            print_info("update sql example:'update staff_table set age=33 where dept = Market'", "error")
            return False
    elif condition == 'del':
        if re.match("del[ ]+from[ ]+[^ ]+[ ]+where.*", input_sql) is None:
            print_info("del sql example:del from staff_table where staff_id = 10", "error")
            return False
    elif condition == 'add':
        if re.match("add[ ]+[^ ]+[ ]+[^ ]+", input_sql) is None:
            print_info("add sql example:add staff_table Mon,18,13678789527,IT,2018-12-11", "error")
            return False
    return True


# 定义main函数，程序主入口
def main():
    while 1:
        condition_list = {
            'find': find_condition,
            'del': del_condition,
            'update': update_condition,
            'add': add_condition
        }

        all_staff_db = load_db()
        input_sql = input("please input your sql:")
        if "where" in input_sql:
            where_data = where_condition_data(input_sql, all_staff_db)
            # please input your sql:select age from staff_db where name=Jack Wang
            # where_data {'13451024608': {'id': '2', 'name': 'Jack Wang', 'age': '18', 'phone': '13451024608',
            # 'dept': 'HR', 'enrolled_date': '2015-01-07\n'}}
        else:
            where_data = all_staff_db

        if where_data is None:
            continue
        for condition in condition_list:

            if input_sql.startswith(condition):
                if verify_sql(condition, input_sql):
                    condition_list[condition](where_data, input_sql, all_staff_db)
                    break
        else:
            print_info("input sql error", "error")


# 执行main函数
if __name__ == '__main__':
    main()
