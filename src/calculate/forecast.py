# coding=utf8
__author__ = 'Administrator'

import pandas
import tushare
import os
import sys
import time
import numpy
import math
import re

_DATE_FORMAT_STR = '%Y%m%d'
_TIME_FORMAT_STR = '%Y%m%d%H%M%S'
_DATA_PATH_ROOT = 'D:/tmp/personal/data'
_MY_STOCKS = ['600570', '300377']
_SINGLE_STOCK_HISTORY_DATA_BEGIN = '2014-01-01'
_SECTION = 5
_LAST_M_DAYS = 30
_FUTURE_N_DAYS = 1
_TO_FORECAST_DAYS = [1, 3, 5]
# 增加字段，上、下影线和实体线
_ADD_COLUMNS_BY_ROW = {'up_tail_len': ['high', ['close', 'open', 'max'], '-'],
                       'down_tail_len': [['close', 'open', 'min'], 'low', '-'],
                       'entity_len': ['open', 'close', '-'],
                       'up_tail_len_scale': ['up_tail_len', 'entity_len', '/'],
                       'down_tail_len_scale': ['down_tail_len', 'entity_len', '/']}

'''
    # 增加字段，过去N天的整体走势
    将每天走势分成M（比如:5)个切片，幅度为-2～2（-2，-1，0，1，2），
    统计过去N天（比如：3），
    结果就是[-2,2,0]
'''
_ADD_COLUMNS_BY_HISTORY = {}
_FORMAT_COLUMNS_BASE = ['volume', 'price_change']
_FORMAT_COLUMNS_DICT = {}.fromkeys(_FORMAT_COLUMNS_BASE)


def next_days_rise(stockid, m=_LAST_M_DAYS, n=_FUTURE_N_DAYS, start_day=None, linked_stock_ps_data=None):
    # 拼接数据文件全路径
    sh_d_filepath = os.path.join(os.path.join(_DATA_PATH_ROOT, 'DP'), 'sh_D.csv')
    # 读取数据
    sh_d_data_pandas = pandas.read_csv(sh_d_filepath, index_col='date')
    # 生命被格式化的列的对象

    for k in _FORMAT_COLUMNS_DICT:
        # 获取被格式化数据列的数组
        _FORMAT_COLUMNS_DICT[k] = format_dimension_value_list(sh_d_data_pandas.get(k).tolist())
    print 'format_columns_dict ok'

    for key in _FORMAT_COLUMNS_DICT:
        print key, _FORMAT_COLUMNS_DICT[key]
    index_list = sh_d_data_pandas.index.tolist()
    # 生成数据切片分组
    # 刷新元数据
    for index in index_list:
        for k in _FORMAT_COLUMNS_DICT:
            sh_d_data_pandas.loc[index][k] = get_format_dimension_value(_FORMAT_COLUMNS_DICT[k],
                                                                        sh_d_data_pandas.loc[index][k])
    print "flush orign data ok"

    # 初始化结果res
    res = {}
    # to_caculate_size = sh_d_data_pandas.iloc.size
    for column_name in _FORMAT_COLUMNS_BASE:
        # all_format_dimension_value = {}.fromkeys(sh_d_data_pandas.get(column_name).tolist()).keys()
        all_format_dimension_value = []
        for item in range(_SECTION):
            all_format_dimension_value.append(float(item))

        '''
            res 的格式
            res = {'volum':
                        {1day:obj,3day:obj...},
                    'price_change':{}}
            obj：_SECTION*_SECTION的矩阵，当前变动值×未来N日可能涨幅
                大概的格式：
    |------------------------------------------|
    |           price_change_level             |
    |volum_level|--0---1---2---3---4---5----   |
    |        0  | 70   1  22  22  34  10       |
    |        1  | 10  10  90  10   1   5       |
    |        2  | 10  10  90  10   1   5       |
    |        3  | 10  10  90  10   1   5       |
    |        4  | 10  10  90  10   1   5       |
    |------------------------------------------|
        '''
        res[column_name] = {}
        for day_num in _TO_FORECAST_DAYS:
            res[column_name][day_num] = numpy.zeros((_SECTION, _SECTION))

        '''
        # 原来版本的数据结构
        for format_dimension_value in all_format_dimension_value:
            res[column_name][format_dimension_value] = {}
            # 预设所有可能的level对应的未来1、3、5日的涨幅度
            for day_num in _TO_FORECAST_DAYS:
                res[column_name][format_dimension_value][day_num] = {}
                for temp_value in all_format_dimension_value:
                    res[column_name][format_dimension_value][day_num][temp_value] = 0
        '''
        to_caculate_index_list = sh_d_data_pandas.index
        for i in range(len(to_caculate_index_list)):
            index = to_caculate_index_list[i]
            # try:
            for day_num in _TO_FORECAST_DAYS:
                if (i - day_num) >= 0:
                    '''
                    # 原来数据结构

                    res[column_name][sh_d_data_pandas.loc[index][column_name]][day_num][
                        sh_d_data_pandas.loc[to_caculate_index_list[i - day_num]]['price_change']] += 1
                    '''
                    '''
                    # 逐行处理，
                    index是当前行的索引
                    sh_d_data_pandas.loc[index][column_name] 当前行当前column_name的格式化之后的值
                    sh_d_data_pandas.loc[   to_caculate_index_list[i - day_num]   ]['close']
                                                                                index（date）是倒序的，所以要i-day_num（i之后day_num天），
                                                                                price_change :所有的预测都是针对于未来的price_change
                    sh_d_data_pandas.loc[to_caculate_index_list[i - day_num]]['close'] : N日之后的收盘价格
                    sh_d_data_pandas.loc[to_caculate_index_list[i]]['close'] : 当日收盘价格

                    '''
                    try:
                        if linked_stock_ps_data == None:
                            close_level = get_format_dimension_value(_FORMAT_COLUMNS_DICT['price_change'],
                                                                     sh_d_data_pandas.loc[
                                                                         to_caculate_index_list[i - day_num]][
                                                                         'close'] -
                                                                     sh_d_data_pandas.loc[to_caculate_index_list[i]][
                                                                         'close'])
                        else:
                            close_level = get_format_dimension_value(_FORMAT_COLUMNS_DICT['price_change'],
                                                                     linked_stock_ps_data.loc[
                                                                         to_caculate_index_list[i - day_num]][
                                                                         'close'] -
                                                                     linked_stock_ps_data.loc[
                                                                         to_caculate_index_list[i]]['close'])
                        res[column_name][day_num][
                            int(sh_d_data_pandas.loc[index][column_name])][
                            int(close_level)] += 1
                    except Exception, e:
                        print e
    '''
    # 将结果格式化成比例
    '''
    for column_name in res:
        for day_num in res[column_name]:
            for cur_value_level in range(_SECTION):
                temp_sum = sum(res[column_name][day_num][cur_value_level])
                for future_p_change in range(_SECTION):
                    res[column_name][day_num][cur_value_level][future_p_change] = \
                        res[column_name][day_num][cur_value_level][future_p_change] / temp_sum
    return res


def format_dimension_value_list(dimension_value_list, section=7):
    format_dimension_list = []
    to_mod = len(dimension_value_list) / section + 1
    j = 0
    for i in range(section):
        format_dimension_list.append([])
    dimension_value_list.sort()
    for i in range(len(dimension_value_list)):
        if i % to_mod == 0:
            format_dimension_list[j].append(dimension_value_list[i])
            if j > 0:
                format_dimension_list[j - 1].append(dimension_value_list[i])
            j += 1
    format_dimension_list[-1].append(max(dimension_value_list))
    return format_dimension_list


def get_format_dimension_value(format_dimension_list, orign_value):
    for i in range(len(format_dimension_list)):
        if orign_value > min(format_dimension_list[i]) and orign_value <= max(format_dimension_list[i]):
            return i
    if orign_value <= min(format_dimension_list[0]):
        return 0
    if orign_value >= max(format_dimension_list[-1]):
        return len(format_dimension_list) - 1


def _get_format_dimension_value(format_dimension_list, orign_value):
    for i in range(len(format_dimension_list)):
        if orign_value <= format_dimension_list[i]:
            return i
    return len(format_dimension_list)


def wight_function(last_m_days, next_days):
    return 1


def get_nextN_days_change_per(value_column_name, value_level, pandas_data_format_res, N=1):
    '''
    # 使用老格式
    values = pandas_data_format_res[value_level][N].values()
    max_value = max(values)
    sum_value = sum(values)
    max_index = pandas_data_format_res[value_level][N].keys()[values.index(max_value)]
    return max_value * 1.0 / sum_value, max_index

    '''
    # 使用矩阵格式
    return pandas_data_format_res[value_column_name][N][
        get_format_dimension_value(_FORMAT_COLUMNS_DICT[value_column_name], value_level)]


def _weight_based_time(days):
    '''
        希望是一个边际递减的的函数
        1、不能是负数
        2、最近N天的效果比较大
        3、近似归一化（先加后除）
        大概满足需求
        for i in range(1, 200):
            print i, _weight_based_time(i)
        1   1.06
        2   0.94
        10  0.67
        100 0.279
        199 0.163
    '''
    r = (math.log(days / 5.0, 0.3) + 3.2) / 4
    if r < 0:
        r = 0
    return r


def forecast_base_function(history_matrix, weight_of_dimension, current_dimension_values):
    '''
    inner param:
        d  ~ dimension
        dv ~ dimension_value
    :param history_matrix:
        {
        hd:{

                d1: { d1p1 : [matrix], d1p2 : [], ... } # 所有数据都和时间有关系
                    ---->
                        { d1p1 : [] * weight_based_time, ....}
                d2: { d2p1 : [], d2p2 : [], ... }
                ...
            }
        mv:{
                d1:[ [], [], [], ... ],
                d2:[]
                ...
            }
        }
    :param weight_of_dimension:
        d1: wd1, b: wd2, ...
    :param current_dimension_values:
        {d1: dv1, d2: dv2, ...}
    :return:
        [0.x, 0.x, 0.x, ...]
    '''
    res = {}
    based_time_list = []
    time_weight = {}
    for d in history_matrix['hd']:
        for k in history_matrix['hd'][d]:
            based_time_list.append(k)
    based_time_list = {}.fromkeys(based_time_list).keys()
    for t in based_time_list:
        time_weight[t] = _weight_based_time(t)

    for d in history_matrix['hd']:
        for t in history_matrix['hd'][d]:
            if isinstance(history_matrix['hd'][d][t], list):
                history_matrix['hd'][d][t] = numpy.matrix(history_matrix['hd'][d][t])
            history_matrix['hd'][d][t] = history_matrix['hd'][d][t] * time_weight[t] * weight_of_dimension[d]
            dimension_format_value = _get_format_dimension_value(history_matrix['mv'][d], current_dimension_values[d])
            if res.keys().count(d) == 0:
                res[d] = history_matrix['hd'][d][t][dimension_format_value]
            else:
                res[d] = res[d] + history_matrix['hd'][d][t][dimension_format_value]
    x = None
    for v in res.values():
        if x is None:
            x = v
        else:
            x += v
    x = x.tolist()[0]
    s = sum(x)
    return [i / s for i in x]


'''
    test code

h = {
    'hd': {
        'a': {
            10: numpy.matrix([[2, 3, 3], [3, 1, 4], [7, 0, 1]]),
            20: numpy.matrix([[5, 5, 5], [7, 2, 6], [2, 10, 3]])
        },
        'b': {
            10: numpy.matrix([[2, 3, 2], [3, 1, 3], [6, 0, 1]]),
            20: numpy.matrix([[9, 3, 3], [3, 8, 4], [7, 7, 1]])
        }
    },
    'mv': {
        'a': [10, 20],
        'b': [1, 4]
    }
}
w = {'a': 2.0, 'b': 1.2}
cv = {'a': 20, 'b': 15}

res = forecast_base_function(h, w, cv)
print res

# for i in range(1, 200):
#     print i, _weight_based_time(i)
'''

def _get_full_filename(filepath, stock_code, ktype):
    '''

    :param
    filepath:
    :param
    stock_code:
    :param
    ktype:
    :return:
    '''
    full_filename = ''
    search = '_'.join([stock_code, ktype])
    for filename in os.listdir(filepath):
        if filename.startswith(search):
            return os.path.join(filepath, filename)

    return full_filename


def _analytics_history_data(conf, stock_code, type=0, ktype='D', start=None, end=None):
    '''

    :param
    stock_code:
    :param
    type:
    0: matrix
    1: list
    :param
    ktype:
    d: 日线
    :param
    start:
    :param
    end:
        :return:
        '''
    stock_history_data = {'hd': {}, 'mv': {}}
    dp_filepath = os.path.join(conf.dataConfig.data_root_path, conf.dataConfig.dp_dir)
    stock_data_path = os.path.join(conf.dataConfig.data_root_path, conf.dataConfig.stock_data_dir)
    stock_code = str(stock_code)
    r = re.compile('^\d*')

    if stock_code.__len__() == 6:
        if stock_code[0] in ['6', '3']:
            stock_file_fullname = _get_full_filename(stock_data_path, stock_code, ktype)
        else:
            stock_file_fullname = _get_full_filename(dp_filepath, stock_code, ktype)
    else:
        if re.findall(r, stock_code)[0].__len__() == len(stock_code):
            stock_file_fullname = _get_full_filename(stock_data_path, stock_code.rjust(6, '0'), ktype)
        else:
            stock_file_fullname = _get_full_filename(dp_filepath, stock_code, ktype)
    history_data = _flush_stock_orign_data(stock_file_fullname)
    return history_data


def _flush_stock_orign_data(stock_file_fullname, bench_data=None):
    stock_history_data = pandas.read_csv(stock_file_fullname, index_col='date')
    stock_history_data['price_change'] = numpy.nan
    stock_history_data['top_tail'] = numpy.nan
    stock_history_data['bottom_tail'] = numpy.nan
    stock_history_data['entity'] = numpy.nan
    stock_history_data['volume_change'] = numpy.nan
    for i in range(len(stock_history_data.index)):
        index = stock_history_data.index[i]
        if index != stock_history_data.index.min():
            stock_history_data.loc[index]['price_change'] = (stock_history_data.loc[index]['close'] -
                                                             stock_history_data.loc[stock_history_data.index[i + 1]][
                                                                 'close']) / \
                                                            stock_history_data.loc[stock_history_data.index[i + 1]][
                                                                'close']
            stock_history_data.loc[index]['volume_change'] = stock_history_data.loc[index]['volume'] / \
                                                             stock_history_data.loc[stock_history_data.index[i + 1]][
                                                                 'volume']
        else:
            pass
        stock_history_data.loc[index]['top_tail'] = stock_history_data.loc[index]['high'] - max(
            stock_history_data.loc[index]['open'], stock_history_data.loc[index]['close'])
        stock_history_data.loc[index]['bottom_tail'] = min(
            stock_history_data.loc[index]['open'], stock_history_data.loc[index]['close']) - \
                                                       stock_history_data.loc[index]['low']
        stock_history_data.loc[index]['entity'] = stock_history_data.loc[index]['close'] - \
                                                  stock_history_data.loc[index]['open']

    return stock_history_data


def _format_dimension_values(dimension_values, section=7):
    res = []
    step = len(dimension_values) / section
    if len(dimension_values) < section:
        return None
    for i in range(1, section):
        res.append(dimension_values[i * step])
    return res


    # print _format_dimension_values(range(20), section=5)