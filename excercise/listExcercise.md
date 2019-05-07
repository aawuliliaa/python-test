
##### 1.创建一个空列表，命名为names,往里面添加old_driver,rain,jack,shanshan,peiqi,black_girl 元素
```
方法一：手动添加
>>> L2 = []
>>> L2.append("old_driver")
>>> L2.append("rain")
>>> L2.append("jack")
方法二：循环方式
a = "old_driver,rain,jack,shanshan,peiqi,black_girl"
L2 = []
for word in a.rsplit(","):
    L2.append(word)
print(L2)
运行程序
E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
['old_driver', 'rain', 'jack', 'shanshan', 'peiqi', 'black_girl']
```

##### 2.往names列表里black_girl前面插入一个alex
```
>>> names = ['old_driver', 'rain', 'jack', 'shanshan', 'peiqi', 'black_girl']
>>> names.insert(-1,"alex")
```

##### 3.把shanshan的名字改成中文，姗姗
```
>>> names[3] = "珊珊"
>>> names
['old_driver', 'rain', 'jack', '珊珊', 'peiqi', 'alex', 'black_girl']
```

##### 4.往names列表里rain的后面插入一个子列表，[oldboy, oldgirl]
```
>>> names
['old_driver', 'rain', 'jack', '珊珊', 'peiqi', 'alex', 'black_girl', 'boy', 'gril']
>>> names[-1] = ["boy","girl"]
>>> names
['old_driver', 'rain', 'jack', '珊珊', 'peiqi', 'alex', 'black_girl', 'boy', ['boy', 'girl']]
>>>
```


##### 5.返回peiqi的索引值
```
>>> names.index("peiqi")
4
```

##### 6.创建新列表[1,2,3,4,2,5,6,2],合并入names列表
```
>>> names.extend([1,2,3,4,2,5,6,2])
>>> names
['old_driver', 'rain', 'jack', '珊珊', 'peiqi', 'alex', 'black_girl', 'boy', ['boy', 'girl'], 1, 2, 3, 4, 2, 5, 6, 2]
>>>
```

##### 7.取出names列表中索引4-7的元素
```
>>> names[4:7]
['peiqi', 'alex', 'black_girl']
```

##### 8.取出names列表中索引2-10的元素，步长为2
```
>>> names[2:10:2]
['jack', 'peiqi', 'black_girl', ['boy', 'girl']]
```

##### 9.取出names列表中最后3个元素
```
>>> names[-3:]
[5, 6, 2]
```


##### 10.循环names列表，打印每个元素的索引值，和元素
```
names = ['old_driver', 'rain', 'jack', '珊珊', 'peiqi', 'alex', 'black_girl', 'boy', ['boy', 'girl'], 1, 2, 3, 4, 2, 5, 6, 2]

count = 0
while count < len(names):
    print(count, names[count])
    count += 1

E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
0 old_driver
1 rain
2 jack
3 珊珊
4 peiqi
5 alex
6 black_girl
7 boy
8 ['boy', 'girl']
9 1
10 2
11 3
12 4
13 2
14 5
15 6
16 2

Process finished with exit code 0


names = ['old_driver', '珊珊', ['boy', 'girl']]

for i in enumerate(names):
    print(i)
for index, i in enumerate(names):
    print(index, i)

E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
(0, 'old_driver')
(1, '珊珊')
(2, ['boy', 'girl'])
0 old_driver
1 珊珊
2 ['boy', 'girl']
```


##### 11.循环names列表，打印每个元素的索引值，和元素，当索引值 为偶数时，把对应的元素改成-1
```
names = [ '珊珊', 'peiqi', 'alex', 'black_girl', 'boy', ['boy', 'girl']]

count = 0
while count < len(names):

    if count % 2 == 0:
        names[count] = -1
    print(count, names[count])
    count += 1
	
E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
0 -1
1 peiqi
2 -1
3 black_girl
4 -1
5 ['boy', 'girl']

Process finished with exit code 0
```



##### 12.names里有3个2，请返回第2个2的索引值。不要人肉数，要动态找(提示，找到第一个2的位置，在此基础上再找第2个)
```
names = [ '珊珊', 2, 'alex', 'black_girl', 2, ['boy', 'girl']]
first_two_index = names.index(2)
second_two_index = names[first_two_index+1:].index(2)
print(first_two_index+second_two_index+1)

E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
4
```
##### 13.现有商品列表如下:
    products = [ ['Iphone8',6888],['MacPro',14800], ['小米6',2499],['Coffee',31],['Book',80],['Nike Shoes',799] ]
    需打印出这样的格式：

    ---------商品列表----------
    0. Iphone8    6888
    1. MacPro    14800
    2. 小米6    2499
    3. Coffee    31
    4. Book    80
    5. Nike Shoes    799

##### 14. 写一个循环，不断的问用户想买什么，用户选择一个商品编号，就把对应的商品添加到购物车里， 最终用户输入q退出时，打印购物车里的商品列表
后面两个题目在homework/shop中已经书写，这里不再赘述