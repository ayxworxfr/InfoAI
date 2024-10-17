import random

NUM = "0123456789"


# 生成指定位数随机数字
def random_str(n: int) -> str:
    result = ""
    for i in range(n):
        c = random.choice(NUM)
        if i == 0 and c == "0":
            continue
        else:
            result += c

    return result
