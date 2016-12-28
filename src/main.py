# coding=utf8
__author__ = 'Administrator'

import pandas
import tushare
import os
import sys
import time
from spider import historyData
import numpy
from calculate import forecast
from calculate import subnew
from globalFactory import configFectory
import threading
import thread
import Queue


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

# _FORMAT_COLUMNS = ['volume', 'price_change', 'up_tail_len', 'down_tail_len', 'entity_len']


def collect_history_data():
    '''
        获取关注股票的日线数据
    :return:
    '''
    # 获取最新的股票基础数据
    historyData.get_stock_base(_DATA_PATH_ROOT, _DATE_FORMAT_STR)
    # 获取大盘数据
    historyData.get_dp_history_data(_DATA_PATH_ROOT, _TIME_FORMAT_STR, _DATE_FORMAT_STR)
    # 获取个股数据
    historyData.get_stock_history_data(_DATA_PATH_ROOT, _DATE_FORMAT_STR, _TIME_FORMAT_STR, _MY_STOCKS)
    # 获取新股数据
    subnewstock_pool = subnew.get_subnewstock_list(_DATA_PATH_ROOT, _DATE_FORMAT_STR)


stock_code_queue = Queue.Queue()
mylock = thread.allocate_lock()
import random


def spider_stock():
    conf = configFectory.config_class()
    global stock_code_queue
    while (not stock_code_queue.empty()):
        mylock.acquire()
        stock_code = stock_code_queue.get()
        mylock.release()
        historyData.get_stock_history_data(conf, stock_code, is_start_new_request=True)
        print stock_code, 'ok'
        # time.sleep(random.random())


def use_threading():
    global stock_code_queue
    stock_base_info = pandas.read_csv('d:/tmp/personal/data/base/stockbase_20161101.csv', index_col='code')
    for stock_code in stock_base_info.index:
        stock_code_queue.put(str(stock_code).rjust(6, '0'))
    thread_size = 10
    threads = []
    for i in range(thread_size):
        t = threading.Thread(target=spider_stock, name='thread-' + str(i))
        threads.append(t)
    for t in threads:
        t.start()


def useThreading():
    conf = configFectory.config_class()
    threads = []
    favorite_stocks = []
    threads.append(target=historyData.get_stock_base, group='spider',
                   name='-'.join('spider', 'stock_base'), args=(conf,))
    threads.append(target=historyData.get_dp_history_data, group='spider',
                   name='-'.join('spider', 'dp'), args=(conf,))
    threads.append(target=historyData.get_hgt_history_data, group='spider',
                   name='-'.join('spider', 'dp'), args=(conf,))
    threads.append(target=forecast.get_nextN_days_change_per, group='calc',
                   name='-'.join('calc', 'dp'), args=(conf,))
    threads.append(target=forecast.hgt_(), group='calc',
                   name='-'.join('calc', 'hgt'), args=(conf,))
    for i in range(len(favorite_stocks)):
        threads.append(target=forecast.get_favorite_stocks, group='calc',
                       name='-'.join('calc', 'stock', favorite_stocks[i]), args=(conf, favorite_stocks[i]))
        threads.append(target=historyData.get_stock_history_data(), group='spider',
                       name='-'.join('spider', 'dp'), args=(conf, favorite_stocks[i]))
    for thread in threads:
        thread.start()


if __name__ == '__main__':
    # 获取历史数据
    # collect_history_data()
    '''
        caculate

    t = forecast.next_days_rise(_MY_STOCKS[0])

    # for k in t:
    # for kk in t[k]:
    # print k, kk, t[k][kk]

    # 今天下跌 25.97
    today_price_change = 25.97
    print forecast.get_nextN_days_change_per('price_change', today_price_change, t, 1)
    print forecast.get_nextN_days_change_per('price_change', today_price_change, t, 3)
    print forecast.get_nextN_days_change_per('price_change', today_price_change, t, 5)
    '''
    # useThreading()
    # print len(subnew_dict[max(subnew_dict.keys())])
    conf = configFectory.config_class()
    # subnew_dict = subnew.get_subnewstock_list(conf, )
    hd = forecast._analytics_history_data(conf, '300558', ktype='d')
    print hd.columns
    for column in hd.columns:
        print column,hd[column].max(),hd[column].min()
    print hd.index.size
    # stock_base_info = pandas.read_csv('d:/tmp/personal/data/base/stockbase_20161101.csv', index_col='code')
    # for stock_code in stock_base_info.index:
    # historyData.get_stock_history_data(conf, stock_codes=stock_code, is_start_new_request=True)
