# coding=utf8
__author__ = 'Administrator'
import tushare
import pandas
from spider import historyData
from datetime import datetime


def get_subnewstock_list(config, send_new_request=False):
    '''
        90:3个月内
        180：半年内
        365：一年内
    :param args:
    :return:
        返回不同周期内上市的code清单
    '''
    data_root_path = config.dataConfig.data_root_path
    date_format_str = config.dataConfig.date_format_str
    time_format_str = config.dataConfig.time_format_str
    subnewstock_level = config.subnew.subnewstock_level

    stock_basic_file_name = historyData.get_stock_basic_file_name(data_root_path, date_format_str)
    stock_basic_data = pandas.read_csv(stock_basic_file_name, index_col='code')
    today = datetime.today()
    subnewstock_pool = {}
    found_stock_codes = []
    for index in stock_basic_data.index:
        stock_code = index
        # try:
        if True:
            try:
                stock_timeToMarket = datetime.strptime(str(stock_basic_data.loc[index]['timeToMarket']),
                                                       date_format_str)
            except:
                stock_timeToMarket = today
            for level in subnewstock_level:
                if found_stock_codes.count(stock_code) == 0:
                    if (today - stock_timeToMarket).days <= level:
                        if subnewstock_pool.keys().count(level) > 0:
                            subnewstock_pool[level].append(stock_code)
                        else:
                            subnewstock_pool[level] = [stock_code]
                    found_stock_codes.append(stock_code)
    if send_new_request:
        for stock_code in subnewstock_pool[max(subnewstock_pool.keys())]:
            historyData.get_stock_history_data(config, stock_codes=stock_code,
                                               is_start_new_request=True)
    return subnewstock_pool


def subnew_limitup_open(config, subnew_obj, ):
    '''
        查看开板后N日内的最大跌幅和最大涨幅，以及出现的日期
    :return:
        code,price_to_market,limitup_open_use_days,total_increase_rate,
    '''

    pass

