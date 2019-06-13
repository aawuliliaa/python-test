count = 0
same_user = True
last_user = None
f = open("account.txt", "r")
# accounts = {'vita': ['123456', 0], 'lyly': ['1234567', 0]}
# f.read()读出的是字符串，"{'vita': ['123456', 0], 'lyly': ['1234567', 0]}"
# 我们要将其转换为字典进行操作，所以使用eval()
accounts = eval(f.read())
while count < 3:
    name = input("please input your name:").strip()
    password = input("please input your password:").strip()

    if last_user is None:
        last_user = name
    if last_user != name:
        same_user = False

    # 如果用户存在
    if name in accounts:
        lock_status = accounts[name][1]
        # 如果用户没有锁定
        if lock_status == 0:
            if password == accounts[name][0]:
                print("welcome come here!")
                exit()
            else:
                print("your password is incorrect!")
        # 用户被锁定了
        else:
            print("this user has been locked!")
    # 用户不存在
    else:
        print("there is not this user!")
    # 记录用户已经输入一次了
    count = count + 1
    # 这里要重新给last_user赋值，否则last_user存储的永远是第一次用户输入的名字，不是真正意义的上一次用户名
    last_user = name
else:
    print("you have tried too many times!")
    # 1.由于可能用户三次输入的用户名都是相同的不存在的用户，用户不存在，设置锁定状态会报keyError
    # 2.可能三输入的都是锁定的用户，所以判断accounts[last_user][1] == 0锁定状态，为0，才进行写入锁定状态，
    # 为1，就没必要再打开文件重新写入了
    # 虽然系统已经进行了友好的页面提示，但是用户的行为是任意的，所以程序尽量考虑到用户的多种操作行为
    # 3.三次一样要是输入相同，所以判断same_user is True,并且把该条件放在最前面，该条件不符合，后面的就不判断了
    # 该种设置方法，主要是为了尽可能减少程序执行无用的代码
    if same_user is True and last_user in accounts and accounts[last_user][1] == 0 :
        accounts[name][1] = 1
        f = open("account.txt", "w")
        # 写到硬盘上的
        f.write(str(accounts))
        f.close()
        print("there is something wrong with the same username for three times,we will lock it!")

