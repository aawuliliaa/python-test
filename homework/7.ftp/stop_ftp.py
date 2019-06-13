#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita

import re

import subprocess
cmd_obj = subprocess.Popen('tasklist|findstr "python"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout = cmd_obj.stdout.read()
stderr = cmd_obj.stderr.read()
pid_Console_list = re.findall("[0-9]+[ ]Console", stdout.decode("gbk"))

if pid_Console_list:

    for pid_Console in pid_Console_list:
        pid=int(re.search("[0-9]+", pid_Console).group())
        # print(pid.group(),type(pid.group()))
        kill_cmd_obj = subprocess.Popen('taskkill /PID %s -t -f' % pid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kill_stdout = kill_cmd_obj.stdout.read()
        kill_stderr = kill_cmd_obj.stderr.read()
        print((kill_stderr+kill_stdout).decode("gbk"))
