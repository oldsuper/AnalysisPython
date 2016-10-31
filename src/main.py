# coding=utf8
__author__ = 'Administrator'

import pandas
import tushare
import os
import sys
import time
from spider import historyData

_DATA_PATH_ROOT = 'D:/tmp/personal/data'
_MY_STOCKS = ['600570', '300377']
_SINGLE_STOCK_HISTORY_DATA_BEGIN = '2014-01-01'
_SECTION = 10
_LAST_M_DAYS = 30
_FUTURE_N_DAYS = 1


def collect_history_data():
    historyData.fetchStockBase(os.path.join(_DATA_PATH_ROOT, 'base'))
    historyData.DP(os.path.join(_DATA_PATH_ROOT, 'DP'))
    for stock in _MY_STOCKS:
        historyData.getHistoryData(os.path.join(_DATA_PATH_ROOT, 'stocks'), stock,
                                   start=_SINGLE_STOCK_HISTORY_DATA_BEGIN)


def next_days_rise(stockid, m=_LAST_M_DAYS, n=_FUTURE_N_DAYS, start_day=None):
    # 拼接数据文件全路径
    sh_d_filepath = os.path.join(os.path.join(_DATA_PATH_ROOT, 'DP'), 'sh_D.csv')
    # 读取数据
    sh_d_data_pandas = pandas.read_csv(sh_d_filepath, index_col='date')
    # 获取被格式化数据列的数组
    format_volume_list = format_dimension_value_list(sh_d_data_pandas.get('volume').tolist())
    print 'format_volume_list ok'
    index_list = sh_d_data_pandas.index.tolist()
    # 生成数据切片分组
    for index in index_list:
        sh_d_data_pandas.loc[index]['volume'] = get_format_dimension_value(format_volume_list,
                                                                           sh_d_data_pandas.loc[index]['volume'])
    # 将元数据切片
    res = {}
    to_caculate_size = sh_d_data_pandas.iloc[m:0 - n].size
    for format_dimension_value in {}.fromkeys(sh_d_data_pandas.get('volume').tolist()).keys():
        # 这里的数据不对，全部是“当前”日期的，而我要的是N日后的
        # res[format_dimension_value] = 1.0 * sh_d_data_pandas.iloc[m:0 - n][
        #     sh_d_data_pandas.iloc[m:0 - n]['volume'] == format_dimension_value].size / to_caculate_size
        res[ format_dimension_value ] =
    return res


'''
def next_days_rise(last_m_days, next_days, format_dimension_value, for_type):
    pass
'''


def format_dimension_value_list(dimension_value_list, section=_SECTION):
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


def wight_function(last_m_days, next_days):
    return 1


if __name__ == '__main__':
    # collect_history_data()
    t = next_days_rise(_MY_STOCKS[0])
    print max(t.values()) / min(t.values())