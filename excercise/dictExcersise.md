##### 1.请循环遍历所有的key
```
dic = {'k1': 'v1', 'k2': 'v2'}
for k in dic:
    print(k)
E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
k1
k2
```
##### 2.请循环遍历所有的value
```
dic = {'k1': 'v1', 'k2': 'v2'}
for k in dic:
    print(dic[k])
E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
v1
v2
```
##### 3.请循环遍历所有的key,value
```
dic = {'k1': 'v1', 'k2': 'v2'}
for k in dic:
    print(k,dic[k])
E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
k1 v1
k2 v2
```
##### 4.在字典中添加一个键值对k4:v4,输出添加后的字典
```
>>> dic["k4"]="v4"
>>> dic
{'k1': 'v1', 'k2': 'v2', 'k4': 'v4'}
```
##### 5.删除字典中的键值对k1:v1,并输出删除后的字典
```
>>> del dic["k1"]
>>> dic
{'k2': 'v2', 'k4': 'v4'}

```
##### 6.删除字典中的键k5对应的键值对，如果字典中不存在键k5,则不报错，并且让其返回None
```
dic.pop("k8",None)

```
##### 7.请获取字典中"k2"对应的值
```
>>> dic["k2"]
'v2'

```
##### 8.请获取字典中"k6"对应的值,如果不存在，则不报错，并且让其返回None。
```
>>> dic.get("k6")
>>>

```
##### 9.现有dict2 = {"k1":"v11","a":"b"},通过一行操作使dict2 = {"k1":"v1","k2":"v2","k3":"v3","a":"b"}
```
>>> dict2 = {"k1":"v11","a":"b"}
>>> dict2.update({"k3":"v3"})
>>> dict2
{'k1': 'v11', 'a': 'b', 'k3': 'v3'}

```
##### 10.组合嵌套题。写代码，有如下列表，按照要求实现每一个功能

```
"""
lis = [["k",["qwe",20,{"k1":["tt",3,"1"]},89],"ab"]]
10.1、将列表中的tt变成大写(用两种方法)
10.2、将列表中的字符串"1"变成数字101(用两种方法)
"""
>>> list[0][1][2].get("k1")[0].upper()
'TT'
>>> list[0][1][2].get("k1")[0].swapcase()
'TT'

方法一：
>>> list[0][1][2]["k1"][0] = "100"
>>> list
[['k', ['qwe', 20, {'k1': ['100', 3, '1']}, 89], 'ab']]
方法二：
>>> list = [["k",["qwe",20,{"k1":["tt",3,"1"]},89],"ab"]]
>>> list[0][1][2].get("k1")[0] = "100"
>>> list
[['k', ['qwe', 20, {'k1': ['100', 3, '1']}, 89], 'ab']]
>>>

```
##### 11.按照需求实现如下功能
```
"""
现有一个列表li = [1,2,3,'a',4,'c'],有一个字典(此字典是动态生成的，你并不知道他里面有多少
键值对，所以用dic={}模拟字典；现在需要完成这样的操作：如果该字典没有"k1"这个键，那就创建
这个"k1"键和对应的值(该键对应的值为空列表)，并将列表li中的索引位为奇数对应的元素，添加到
"k1"这个键对应的空列表中。如果该字典中有"k1"这个键，且k1对应的value是列表类型。那就将该列表li
中的索引位为奇数对应的元素，添加到"k1"，这个键对应的值中。
"""
li = [1, 2, 3, 'a', 4, 'c']

dic = {'k1': [2]}
new_li = []
count = 0
while count < len(li):
    if count % 2 == 1:
        new_li.append(li[count])
    count += 1
if "k1" in dic:
    if isinstance(dic.get("k1"), list):
        dic.get("k1").extend(new_li)

else:
    dic.setdefault("k1", new_li)
print(dic)

E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
{'k1': [2, 2, 'a', 'c']}

li = [1, 2, 3, 'a', 4, 'c']

dic = {'k6': [2]}
new_li = []
count = 0
while count < len(li):
    if count % 2 == 1:
        new_li.append(li[count])
    count += 1
if "k1" in dic:
    if isinstance(dic.get("k1"), list):
        dic.get("k1").extend(new_li)

else:
    dic.setdefault("k1", new_li)
print(dic)

E:\PythonProject\python-test\venvP3\Scripts\python.exe E:/PythonProject/python-test/BasicGrammer/test.py
{'k6': [2], 'k1': [2, 'a', 'c']}

```

