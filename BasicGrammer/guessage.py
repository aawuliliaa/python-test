"""
猜年龄游戏：
允许用户最多猜三次，猜了三次后，询问是都继续玩，如果输入Y，可以继续猜三次，否则退出
"""
age = 23
count = 0
while count < 3:
    try:
        guess_age = int(input("input the age of you think:"))
    except ValueError:
        print("you should input one number!")
        count = count + 1
        continue

    if guess_age > 23:
        print("the age you input is too big!")
    elif guess_age < 23:
        print("the age you input is too small!")
    else:
        print("excellent!you are right!")
        break
    count = count + 1
    while count == 3:
        your_choice = input("you only have three chances,would you like to continue(Y|y/N|n):")
        if your_choice.lower() == "y":
            count = 0
        elif your_choice.lower() =="n":
            break
        else:
            print("your input is illegal!input again!")
