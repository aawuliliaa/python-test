goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
    {"name": "裙子", "price": 398},
    {"name": "手机", "price": 998}
]
accounts = {'vita': '123456', 'lyly': '1234567'}
goods_count = 0
shopping_car = {}
# 使用数据字典的形式，更便于获取数据
# shopping_car = {
#     "手机": {"price": "998", "count": 1},
#     "裙子": {"price": "398", "count": 2},
#     "salary": 2340,
#     "left_salary": 345
#     }
# 存储多人的购物信息
# shopping_cars = {"vita": {
#     "手机": {"price": "998", "count": 1},
#     "裙子": {"price": "398", "count": 2},
#     "salary": 2340,
#     "left_salary": 345
#     }
# }

# 该处代码使用了很多次，所以就建了一个方法


def print_info(shopping_car):
    print("\033[41;1m ------------------shop history------------------- \033[0m")
    # 因为字典是无序的，不能保证salary放在前面，所以循环两次，保证输出的顺序
    for key in shopping_car:
        if key == "salary" or key == "left_salary":
            print(key, shopping_car[key])
    for key in shopping_car:
        if key != "salary" and key != "left_salary":
            print(key, shopping_car[key]["price"], shopping_car[key]["count"])
    print("\033[41;1m ------------------shop history------------------- \033[0m")


while True:
    name = input("please input your name:").strip()
    if name in accounts:
        password = input("please input your password:").strip()
        if password == accounts[name]:
            f = open("shop_history.txt", "r", encoding="utf-8")
            # 转换为字典类型
            shopping_cars = eval(f.read())
            if name in shopping_cars:
                shopping_car = shopping_cars[name]
                # 输出购物历史
                print_info(shopping_car)
                while True:
                    # 询问是否有新工资加入
                    has_more_salary = input("do you have some extra salary to be added![Y/y|N/n]:").strip()

                    if has_more_salary.lower() == "y":
                        extra_salary = input("please add some extra salary:").strip()
                        if extra_salary.isdigit():
                            # 有新工资加入，要更新salary和left_salary
                            shopping_car["salary"] += int(extra_salary)
                            shopping_car["left_salary"] += int(extra_salary)
                            # 用于后面的比较和计算
                            left_salary = shopping_car["left_salary"]
                            print_info(shopping_car)
                            break
                        else:
                            # 输入必须是数字
                            print("your extra salary added must be a number!")
                            continue
                    elif has_more_salary.lower() == 'n':
                        # 用于后面的比较和计算
                        left_salary = shopping_cars[name]["left_salary"]
                        break
                    else:
                        print("illegal input,you can just input [Y/y|N/n]!")
                        continue

            else:
                while True:
                    salary = input("you are a new person,please input your salary:").strip()

                    if salary.isdigit():
                        salary = int(salary)
                        left_salary = salary
                        shopping_car.setdefault("salary", salary)
                        break
                    else:
                        print("your salary should be a number!")
                        continue
            print("\033[42;1m **************goods info***************** \033[0m")
            while goods_count < len(goods):
                print(goods_count, goods[goods_count]["name"], goods[goods_count]["price"])
                goods_count += 1
            print("\033[42;1m **************goods info***************** \033[0m")
            while True:

                your_choice = input("you can input one number to buy a goods or 'q' to quit this program:").strip()
                if your_choice.isdigit():
                    your_choice = int(your_choice)
                    if your_choice < len(goods):
                        if left_salary > goods[your_choice]["price"]:
                            goods_name = goods[your_choice]["name"]
                            goods_price = goods[your_choice]["price"]
                            # 如果该商品已经存在，就把数量加1，不存在就设置

                            if goods_name in shopping_car:
                                shopping_car[goods_name]["count"] += 1
                            else:

                                shopping_car.setdefault(goods_name, {})
                                shopping_car[goods_name].setdefault("price", goods[your_choice]["price"])
                                shopping_car[goods_name].setdefault("count", 1)
                            # 购买了商品后，更新剩余工资
                            left_salary = left_salary - goods[your_choice]["price"]
                            shopping_car["left_salary"] = left_salary

                            print_info(shopping_car)
                        else:
                            print("your salary is not enough!")
                            continue
                    else:
                        print("there is not this number goods!")
                        continue
                elif your_choice == 'q':

                    print_info(shopping_car)
                    shopping_cars.setdefault(name, shopping_car)
                    f = open("shop_history.txt", "w", encoding="utf-8")
                    f.write(str(shopping_cars))

                    exit()
                else:
                    print("your input is illegal,input again!")
                    continue

        else:
            # 密码不正确
            print("invalid password!please check your password!")
    else:
        # 用户输入的用户名不存在
        print("invalid username,you need input again!")