# coding=utf8
__author__ = 'gaosongbo'

import tushare
import pandas
import os
from datetime import datetime, timedelta
import numpy


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
    AllData.to_csv(filename)


def getLast3YearsData(datapath, sid):
    '''

    :param datapath:
    :param sid:
    :return:
    '''
    tushare.get_hist_data(sid).to_csv(os.path.join(datapath, sid + '.csv'))


def fetchStockBase(datapath):
    '''

    :param datapath: 放在conf目录下
    :return:
    '''
    tushare.get_stock_basics().to_csv(os.path.join(datapath, 'stockbase.csv'))


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
            toSaveData['p_change_level'] = numpy.nan
            toSaveData['volume_level'] = numpy.nan
            toSaveData.to_csv(tmpffn)
    else:
        tmpffn=ffn
        toSaveData = tushare.get_hist_data(code=sid, ktype=ktype)
        toSaveData['p_change_level'] = numpy.nan
        toSaveData['volume_level'] = numpy.nan
        toSaveData.to_csv(ffn)


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
            pandas.concat([op, np]).drop_duplicates().to_csv(ffn[:0 - len('.bak.csv')])
            os.remove(ffn)