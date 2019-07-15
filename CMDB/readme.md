# 1.环境准备
```
1.把本地代码上传到linux上
https://blog.51cto.com/10983441/2380368
最后一条1.11配置，本地代码上传到linux上
2.linux系统
python安装
cd /opt
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xf Python-3.6.3.tar.xz
cd /opt/Python-3.6.3/
./configure
yum install gcc-c++ gcc -y  #安装编译所需依赖
make  && make install

3.配置环境变量
cat /etc/profile
export PATH=$PATH:/usr/local/python3/bin/
生效
source /etc/profile

接下来就可以验证
[root@m01 opt]# python3
Python 3.6.3 (default, Jul 15 2019, 09:46:16) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-23)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
[root@m01 opt]# pip3

Usage:   
  pip <command> [options]

```