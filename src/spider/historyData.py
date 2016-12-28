# coding=utf8
__author__ = 'gaosongbo'

import tushare
import pandas
import os
from datetime import datetime, timedelta
import numpy

_STOCKBASE_FILEPATH = 'D:/tmp/personal/data/base/stockbase.csv'


def getNewStock(stockbase=''):
    '''
    :param stockbase:
    :return:
    '''
    # 60天内的算新股
    NEWSTOCKPERIOD = 60
    newStockIDs = []
    if os.path.isfile(stockbase):
        sb = pandas.read_csv(stockbase)
        sb = sb.sort_index(by='timeToMarket')
        sbcount = sb.index.size
        today = datetime.today()
        for i in range(sbcount)[::-1]:
            try:
                if (today - datetime.strptime(str(sb.iloc[i - sbcount]['timeToMarket']),
                                              '%Y%m%d')).days <= NEWSTOCKPERIOD:
                    # print ,sb.iloc[i-sbcount]['timeToMarket']
                    newStockIDs.append('%06.d' % sb.iloc[i - sbcount]['code'])
            except:
                pass
    return newStockIDs


def getStockBase(stockbase):
    '''
    :param stockbase:
    :return:
    '''
    if os.path.isfile(stockbase):
        sb = pandas.read_csv(stockbase)
        return sb
    return None


'''

'''


def get_history_data_new(datapath, sid, start=None, end=None):
    '''

    :param datapath:
    :param sid:
    :param start:
    :param end:
    :return:
    '''

    stock_file_fullname = os.path.join(datapath, str(sid) + '.csv')
    if not os.path.isfile(stock_file_fullname):
        stock_ps_data = pandas.read_csv(stock_file_fullname, index_col='date')
        start = stock_ps_data.index.max()
    else:
        if start == None:
            start = pandas.read_csv(_STOCKBASE_FILEPATH, index_col='code').loc[int(sid)]

    return stock_file_fullname


def getHistoryData(datapath, sid, start=None, end=None):
    '''

    :param datapath:
    :param sid:
    :param start:
    :param end:
    :return:
    '''
    DAYFORMAT = '%Y-%m-%d'
    MAXINTERVAL = 365 * 3
    totalData = []
    if end == None:
        end = datetime.strftime(datetime.today(), DAYFORMAT)

    endday = end

    if (datetime.strptime(end, DAYFORMAT) - datetime.strptime(start, DAYFORMAT)).days > MAXINTERVAL:
        startday = datetime.strftime(datetime.strptime(endday, DAYFORMAT) - timedelta(days=MAXINTERVAL), DAYFORMAT)
    else:
        startday = start
    while ( datetime.strptime(startday, DAYFORMAT) >= datetime.strptime(start, DAYFORMAT)):
        # 分成三年三年这种调用方式，然后汇总
        temp = tushare.get_h_data(sid, start=startday, end=endday)
        totalData.append(temp)
        endday = startday
        startday = datetime.strftime(datetime.strptime(endday, DAYFORMAT) - timedelta(days=MAXINTERVAL), DAYFORMAT)

    AllData = pandas.concat(totalData)
    filenameX = lambda x: '_'.join(x)
    filename = os.path.join(datapath, filenameX([sid, start, end])) + '.csv'
    AllData.to_csv(filename.lower())


def getLast3YearsData(datapath, sid):
    '''

    :param datapath:
    :param sid:
    :return:
    '''
    tushare.get_hist_data(sid).to_csv(os.path.join(datapath, sid + '.csv').lower())


def fetch_stockbase(datapath):
    '''
        _STOCKBASE_FILEPATH
    :param datapath: 放在conf目录下
    :return:
    '''
    stockbase_filepath = os.path.join(datapath, 'stockbase.csv')
    new_stockbase_data = tushare.get_stock_basics()
    if os.path.isfile(stockbase_filepath):
        if new_stockbase_data.get('timeToMarket').max() == pandas.read_csv(new_stockbase_data):
            pass
    os.remove(stockbase_filepath)
    tushare.get_stock_basics().to_csv(stockbase_filepath.lower())

    stockbase_filename = 'stockbase_' + 'dd'
    for filename in os.listdir(_STOCKBASE_FILEPATH):
        if filename.startswith('stockbase'):
            stockbase_filename = filename
            break


from datetime import datetime, timedelta

DAYFORMAT = '%Y-%m-%d'


def _DP(datapath, sid, ktype):
    '''
        获取不同种类的大盘指数函数
        20160720    改一下，保存临时文件
    :param datapath:
    :param zs:
    :param ktypes:
    :return:
    '''

    # for fn in os.listdir(datapath):
    # if fn.find()
    # for id in zs:
    timestemp = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    ffn = os.path.join(datapath, sid + '_' + ktype + '.csv')
    if os.path.isfile(ffn):
        oldps = pandas.read_csv(ffn, index_col='date')
        # start = datetime.strftime(datetime.strptime(oldps.index.max(), '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d')
        start = datetime.strptime(oldps.index.max().split(' ')[0], '%Y-%m-%d') + timedelta(days=1)
        # 判断现有数据的时间
        if (start - datetime.now()).days >= 0:
            pass
        else:
            tmpffn = ffn + '.bak.csv'
            toSaveData = tushare.get_hist_data(code=sid, ktype=ktype, start=datetime.strftime(start, '%Y-%m-%d'))
            # toSaveData['p_change_level'] = numpy.nan
            # toSaveData['volume_level'] = numpy.nan
            toSaveData.to_csv(tmpffn.lower())
    else:
        tmpffn = ffn
        toSaveData = tushare.get_hist_data(code=sid, ktype=ktype)
        # toSaveData['p_change_level'] = numpy.nan
        # toSaveData['volume_level'] = numpy.nan
        toSaveData.to_csv(ffn.lower())


# 大盘分时数据统计和汇总
def DP(datapath, dps=None, ktypes=None):
    '''

    :param datapath:
    :param dps:
    :param ktypes:
    :return:
    '''
    if dps == None:
        dps = ['sh', 'sz', 'cyb', 'zxb', 'hs300', 'sz50']
    if ktypes == None:
        ktypes = ['D', 'W', 'M', '5', '15', '30', '60']

    if not os.path.isdir(datapath):
        os.mkdir(datapath)

    for dp in dps:
        for ktype in ktypes:
            _DP(datapath, dp, ktype)
            print dp, ktype, 'ok'
    # 合并去重

    for fn in os.listdir(datapath):
        ffn = os.path.join(datapath, fn)
        if fn.find('.bak.csv') > 0:
            op = pandas.read_csv(ffn, index_col='date')
            np = pandas.read_csv(ffn[:0 - len('.bak.csv')], index_col='date')
            pandas.concat([op, np]).drop_duplicates().to_csv(ffn[:0 - len('.bak.csv')].lower())
            os.remove(ffn)


# new 2016 11 8 add
def get_stock_base(config):
    '''
        get the stock basic info
    :param data_root_path:
    :param date_format_str:
    :return:
    '''
    data_root_path = config.dataConfig.data_root_path
    date_format_str = config.dataConfig.date_format_str
    stock_base_path = os.path.join(data_root_path, 'base').lower()
    if not os.path.isdir(stock_base_path):
        os.mkdir(stock_base_path)
    today_date_str = datetime.strftime(datetime.now(), date_format_str)
    stock_startwords = 'stockbase'
    stock_base_file_name = stock_startwords + '_' + today_date_str + '.csv'
    for file_name in os.listdir(stock_base_path):
        if file_name.startswith(stock_startwords):
            stock_base_file_name = file_name
    stock_base_full_file_name = os.path.join(stock_base_path, stock_base_file_name)
    if stock_base_file_name.find(today_date_str) > -1:
        pass
    else:
        stock_base_data = tushare.get_stock_basics()
        stock_base_data.to_csv(stock_base_full_file_name.lower())
    return stock_base_full_file_name


def get_dp_history_data(config, dp_codes=None, ktypes=None):
    '''
        收盘时间每日1500
    :param data_root_path:
    :param date_format_str: dps = ['sh', 'sz', 'cyb', 'zxb', 'hs300', 'sz50']
    :param ktypes: ktypes = ['D', 'W', 'M', '5', '15', '30', '60']
    :return:
    '''
    data_root_path = config.get('data_root_path')
    time_format_str = config.get('time_format_str')
    date_format_str = config.get('date_format_str')
    dp_data_path = os.path.join(data_root_path, 'DP').lower()
    if not os.path.isdir(dp_data_path):
        os.mkdir(dp_data_path)
    if dp_codes == None:
        dp_codes = ['sh', 'sz', 'cyb', 'zxb', 'hs300', 'sz50']
    if ktypes == None:
        ktypes = ['D', 'W', 'M', '5', '15', '30', '60']
    # dp_data_dict = {}
    # for file_name in os.listdir(dp_data_path):
    # dp_code, ktype, last_get_time_str = file_name.split('.')[0].split('_')
    # dp_data_dict[dp_code] = {ktype: [last_get_time_str, file_name]}
    for dp_code in dp_codes:
        for ktype in ktypes:
            this_time_str = datetime.strftime(datetime.now(), time_format_str)
            last_update_dp_file_name = __get_old_file_name(dp_data_path, dp_code, ktype)
            if last_update_dp_file_name is not None:
                last_get_time_str = last_update_dp_file_name.split('.')[0].split('_')[-1]
                # this_time_str = datetime.strftime(datetime.now(), date_format_str)
                if (datetime.strptime(last_get_time_str, time_format_str) - datetime.strptime(
                        (datetime.strftime(datetime.now(), date_format_str) + '150000'),
                        time_format_str)).total_seconds() >= 0:
                    dp_file_name = last_update_dp_file_name
                else:
                    dp_file_name = __get_dp_history_data(dp_data_path, dp_code, ktype, this_time_str,
                                                        last_update_dp_file_name,
                                                        start=last_get_time_str[:8])
            else:
                last_get_time_str = None
                dp_file_name = __get_dp_history_data(dp_data_path, dp_code, ktype, time_format_str,
                                                    last_get_time_str, )
            print dp_file_name, 'ok'
    return 1


def __get_old_file_name(data_path, *args):
    for file_name in os.listdir(data_path):
        if file_name.startswith('_'.join(args)):
            return file_name
    return None


def __get_dp_history_data(dp_data_path, dp_code, ktype, time_format_str, last_update_file_name=None, start=None,
                         end=None):
    '''
        获取数据的实现函数
        get_hist_data
    :return:
    '''
    time_str = datetime.strftime(datetime.now(), time_format_str)
    dp_file_name = dp_code + '_' + ktype + '_' + time_str + '.csv'
    dp_full_file_name = os.path.join(dp_data_path, dp_file_name)
    dp_data = tushare.get_hist_data(dp_code, ktype=ktype, start=start, end=end)
    if last_update_file_name is not None:
        last_update_dp_data = pandas.read_csv(os.path.join(dp_data_path, last_update_file_name), index_col='date')
        dp_data = pandas.concat([last_update_dp_data, dp_data]).drop_duplicates().sort_index(ascending=False)
    dp_data.to_csv(dp_full_file_name.lower())
    if last_update_file_name is not None:
        os.remove(os.path.join(dp_data_path, last_update_file_name))

    return dp_file_name


def get_stock_history_data(config, stock_codes=None, ktype='D',
                           sub_data_path=None, is_start_new_request=False):
    '''

    :return:
    '''
    now_year = datetime.now().year
    data_root_path=config.dataConfig.data_root_path
    date_format_str=config.dataConfig.date_format_str

    if sub_data_path is None:
        stocks_data_path = os.path.join(data_root_path, 'stocks').lower()
    else:
        stocks_data_path = os.path.join(data_root_path, sub_data_path).lower()
    max_days_per_get = 365
    year_begin_day = '-01-01'
    year_end_day = '-12-31'
    if not os.path.isdir(stocks_data_path):
        os.mkdir(stocks_data_path)
    if stock_codes is None:
        return None
    if not isinstance(stock_codes, list):
        stock_codes = [stock_codes]
    stock_basic_file_name = __get_stock_basic_file_name(data_root_path, date_format_str)
    stock_basic_data = pandas.read_csv(stock_basic_file_name, index_col='code')
    today_str = datetime.strftime(datetime.now(), date_format_str)
    for stock_code in stock_codes:
        stock_code = str(stock_code).rjust(6, '0')
        last_stock_file_name = __get_old_file_name(stocks_data_path, stock_code)
        stock_time_to_market = str(stock_basic_data.loc[int(stock_code)]['timeToMarket'])
        if len(stock_time_to_market) == 8:
            stock_time_to_market = '-'.join(
                [stock_time_to_market[:4], stock_time_to_market[4:6], stock_time_to_market[6:]])
        else:
            stock_time_to_market = '-'.join([today_str[:4], today_str[4:6], today_str[6:]])
        stock_file_name = stock_code + '_' + ktype + '_' + today_str + '.csv'
        # try:
        if True:
            if last_stock_file_name is None:
                print stock_code, stock_time_to_market
                start = max(2007, int(stock_time_to_market[:4]))
                stock_data_list = []
                is_begin = 1
                end = start
                temp = tushare.get_h_data(stock_code, start=stock_time_to_market, end=today_str)
                if temp is None:
                    return None
                if temp.size == 0:
                    return None
                try:
                    temp.to_csv(os.path.join(stocks_data_path, stock_file_name).lower())
                except Exception, e:
                    print e, stock_code
                    # while (start <= now_year):
                    # if start + 3 > now_year:
                    # end = now_year
                    #     else:
                    #         end = start + 2
                    #     if is_begin == 0:
                    #         temp = tushare.get_h_data(stock_code, start=str(start) + year_begin_day,
                    #                                   end=str(end) + year_end_day)
                    #         is_begin += 1
                    #     else:
                    #         temp = tushare.get_h_data(stock_code, start=str(start) + year_begin_day,
                    #                                   end=str(end) + year_end_day)
                    #     if (temp is not None) and (len(temp) > 0):
                    #         stock_data_list.append(temp)
                    #     start = end + 1
                    # if stock_data_list is None:
                    #     return None
                    # if len(stock_data_list) > 0:
                    #     pandas.concat(stock_data_list).drop_duplicates().sort_index(ascending=False).to_csv(
                    #         os.path.join(stocks_data_path, stock_file_name))
                    # else:
                    #     print "error ,stock_data_list.len == 0"
            else:
                # 如果存在文件，则不新发起请求
                if is_start_new_request:
                    return stock_file_name
                # 超过三年的不管
                last_get_day_str = last_stock_file_name.split('.')[0].split('_')[-1]
                new_stock_data = tushare.get_h_data(stock_code, start=last_get_day_str)
                if new_stock_data is None:
                    return stock_file_name
                # 因为index值的数据类型不同存储之后再读出来
                new_stock_data.to_csv(os.path.join(stocks_data_path, stock_file_name).lower())
                new_stock_data = pandas.read_csv(os.path.join(stocks_data_path, stock_file_name), index_col='date')
                old_stock_data = pandas.read_csv(os.path.join(stocks_data_path, last_stock_file_name), index_col='date')
                pandas.concat([new_stock_data, old_stock_data]).drop_duplicates().sort_index(ascending=False).to_csv(
                    os.path.join(stocks_data_path, stock_file_name).lower())
                os.remove(os.path.join(stocks_data_path, last_stock_file_name))
                # except Exception, e:
                # print stock_code, e
    return stock_file_name


def __get_stock_basic_file_name(data_root_path, date_format_str):
    stock_base_path = os.path.join(data_root_path, 'base').lower()
    for file_name in os.listdir(stock_base_path):
        if file_name.startswith('stockbase'):
            return os.path.join(stock_base_path, file_name)
    return get_stock_base(data_root_path, date_format_str)
