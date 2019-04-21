#_*_coding:utf-8_*_

menu = {
    '北京': {
        '海淀': {
            '五道口': {
                'soho': {},
                '网易': {},
                'google': {}
            },
            '中关村': {
                '爱奇艺': {},
                '汽车之家': {},
                'youku': {},
            },
            '上地': {
                '百度': {},
            },
        },
        '昌平': {
            '沙河': {
                '老男孩': {},
                '北航': {},
            },
            '天通苑': {},
            '回龙观': {},
        },
        '朝阳': {},
        '东城': {},
    },
    '上海': {
        '闵行': {
            "人民广场": {
                '炸鸡店': {}
            }
        },
        '闸北': {
            '火车战': {
                '携程': {}
            }
        },
        '浦东': {},
    },
    '山东': {},
}
current_level = menu
# 用于存储上一层的数据。
last_level_list = []
while True:
    for menu_list in current_level:
        print(menu_list)
    your_choice = input("input your choice(b-back to last level|q-quit)").strip()
    if your_choice in current_level:
        # 保存当前层，作为回退时的上一层的数据
        last_level_list.append(current_level)
        # 进入下一层
        current_level = current_level[your_choice]
    elif your_choice == 'b':
        # 长度为0，说明已经在顶层了
        if len(last_level_list) == 0:
            print("you are at the top level!")
        else:
            # 返回列表中的最后一个值，且删除最后一个值
            current_level = last_level_list.pop()
    elif your_choice == 'q':
        exit()
    else:
        # 用户可能的非法输入，包含什么都不输入
        print("your input is illegal!")

