#!/usr/bin/env bash
# centos6系统
#windows上编辑的shelljiaoben ,要在linux上执行dos2unix后才能执行成功
# dos2unix get_host_info.sh
# [root@m01 shell_script]# sh get_host_info.sh
#mem:1990,host_name:m01,disk:30865437,cpu:2
#1.获取CPU信息
## 总核数 = 物理CPU个数 X 每颗物理CPU的核数
## 总逻辑CPU数 = 物理CPU个数 X 每颗物理CPU的核数 X 超线程数
#
## 查看物理CPU个数
#cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l
#
## 查看每个物理CPU中core的个数(即核数)
#cat /proc/cpuinfo| grep "cpu cores"| uniq
#
## 查看逻辑CPU的个数
#cat /proc/cpuinfo| grep "processor"| wc -l
#2.获取总磁盘大小
#[root@m01 crond]# df |grep -v 'Filesystem'| awk -F '[ ]+' '{print $2}'
#9213440
#953128
#194241
#20504628
#[root@m01 crond]# df |grep -v 'Filesystem'| awk -F '[ ]+' 'BEGIN{sum=0}{sum+=$2}END{print sum}'
#30865437
host_name=`hostname`
mem=`free -m|grep 'Mem'|awk -F '[ ]+' '{print $2}'`
disk=`df |grep -v 'Filesystem'| awk -F '[ ]+' 'BEGIN{sum=0}{sum+=$2}END{print sum}'`
cpu=`cat /proc/cpuinfo| grep "processor"| wc -l`
echo "mem:${mem},host_name:${host_name},disk:${disk},cpu:${cpu}"
