#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: vita

# 发送邮件
EMAIL_HOST = 'smtp.163.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 25
EMAIL_HOST_USER = 'linuxengineerofwu@163.com'  # 帐号
EMAIL_HOST_PASSWORD = 'Aaa249400000'  # 密码
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
from django.core.mail import send_mail


# send_mail(
#     "您的文章%s新增了一条评论内容"%article_obj.title,
#     content,
#     settings.EMAIL_HOST_USER,
#     ["916852314@qq.com"]
# )

import threading

t = threading.Thread(target=send_mail, args=("您的文章%s新增了一条评论内容" % "sds",
                                             "sdsdssd",
                                             EMAIL_HOST_USER,
                                             ["1394252416@qq.com@qq.com"])
                     )
t.start()

#
# import smtplib
# # 发送字符串的邮件
# from email.mime.text import MIMEText
# # 处理多种形态的邮件主体我们需要 MIMEMultipart 类
# from email.mime.multipart import MIMEMultipart
# # 处理图片需要 MIMEImage 类
# from email.mime.image import MIMEImage
#
# # 设置服务器所需信息
# fromaddr = 'linuxengineerofwu@163.com'  # 邮件发送方邮箱地址
# password = 'Aaa249400000'  # 密码(部分邮箱为授权码)
# toaddrs = ['linuxengineerofwu@163.com']  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
#
# # 设置email信息
# # ---------------------------发送字符串的邮件-----------------------------
# # 邮件内容设置
# message = MIMEText('hello,ziqiiii', 'plain', 'utf-8')
# # 邮件主题
# message['Subject'] = 'ziqiiii test email'
# # 发送方信息
# message['From'] = "linuxengineerofwu@163.com"
# # 接受方信息
# message['To'] = "linuxengineerofwu@163.com"
#
#
# # 登录并发送邮件
# try:
#     server = smtplib.SMTP('smtp.163.com')  # 163邮箱服务器地址，端口默认为25
#     server.login(fromaddr, password)
#     server.sendmail(fromaddr, toaddrs, message.as_string())
#     print('success')
#     server.quit()
#
# except smtplib.SMTPException as e:
#     print('error', e)  # 打印错误
