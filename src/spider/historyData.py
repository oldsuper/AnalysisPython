# coding=utf8
__author__ = 'gaosongbo'

import tushare
import pandas
import os
from datetime import datetime, timedelta


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
        totalData.append(tushare.get_hist_data(sid, start=startday, end=endday))
        endday = startday
        startday = datetime.strftime(datetime.strptime(endday, DAYFORMAT) - timedelta(days=MAXINTERVAL), DAYFORMAT)

    AllData = pandas.concat(totalData)
    filenameX = lambda x: '_'.join(x)
    filename = os.path.join(datapath, filenameX([sid, start, end])) + '.csv'
    AllData.to_csv(filename)
