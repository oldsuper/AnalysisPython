# coding=utf8
__author__ = 'gaosongbo'

import tushare
import pandas
import os
from datetime import datetime


def getNewStock(stockbase=''):
    # 60天内的算新股
    newStockIDs = []
    if os.path.isfile(stockbase):
        sb = pandas.read_csv(stockbase)
        sb = sb.sort_index(by='timeToMarket')
        sbcount = sb.index.size
        today = datetime.today()
        for i in range(sbcount)[::-1]:
            try:
                if (today - datetime.strptime(str(sb.iloc[i - sbcount]['timeToMarket']), '%Y%m%d')).days <= 60:
                    # print ,sb.iloc[i-sbcount]['timeToMarket']
                    newStockIDs.append('%06.d' % sb.iloc[i - sbcount]['code'])
            except:
                pass
    return newStockIDs


def getHistoryData(datapath, sid, begin, end=None):
    pass