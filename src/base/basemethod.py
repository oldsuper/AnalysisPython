# coding=utf-8

import math
from datetime import datetime


def chunks(arr, n):
    '''
        尽可能平均的等分list
    :param arr: 被等分的list
    :param n: 等分的份数
    :return:
    '''
    m = int(math.ceil(len(arr) / float(n)))
    return [arr[i:i + m] for i in range(0, len(arr), m)]

# chunks 测试代码
# l = range(900000)
# b = datetime.now()
# # print l
# nl = chunks(l, 50000)
# print datetime.now()-b
