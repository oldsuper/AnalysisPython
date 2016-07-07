# coding=utf8
__author__ = 'gaosongbo'
# 仅按需求处理数据获取操作
# 沪股通
# 大盘数据：日、5分钟、15分钟、30分钟
# 个股数据：日、5分钟、15分钟、30分钟
import tushare
import pandas
import numpy
import datetime
from datetime import timedelta
import os

PROJECTPATH = 'd:/\pySpace/AnalysisPython/'
DAYFORMAT = '%Y-%m-%d'


def getToday():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def saomiaoanhao(dataFilepath=None):
    if dataFilepath == None:
        dataFilepath = 'd:/pySpace/data/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_realtime_quotes.csv'
    print dataFilepath
    d = pandas.read_csv(dataFilepath, index_col='code')
    print d[d['a1_v'] == numpy.nan].query('b2_v==b3_v').query('b2_v==b4_v').query('b2_v==b5_v')


def anhaomoxing(sidfp='d:/\pySpace/AnalysisPython/conf/sids.csv'):
    df = tushare.get_realtime_quotes('300312')
    i = 0
    for l in open(sidfp).readlines():
        try:
            if len(l.strip()) > 0:
                sid = l.strip()
                sidd = tushare.get_realtime_quotes(sid)
                df = pandas.concat([df, sidd])
            if i >= 100:
                print l.strip()
                i = 0
            i += 1
        except Exception, e:
            print e, l.strip()
    # del df['name']
    backfile = 'd:/pySpace/data/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_realtime_quotes.csv'
    df.to_csv(backfile, encoding='gbk')
    print "get ok~"
    saomiaoanhao()


def hugutong(
        hgturl='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=DPAB&sty=AHTZJL&js=({data:[(x)],time:%22(ut)%22})&cb=callback02446733516803452&callback=callback02446733516803452&_=1464757205199',
        dateBackupFile='d:/\pySpace/AnalysisPython/data/hgttmp.txt',
        dailyFile='d:/\pySpace/AnalysisPython/data/hgtDailyDetail.csv'):
    import urllib
    import re

    r = re.compile('{.*}')
    content = urllib.urlopen(hgturl).read()
    hgtcont = re.search(r, content).group()
    open(dateBackupFile, 'at+').write(hgtcont + '\n')
    timestr = getToday() + "T" + hgtcont[hgtcont.rfind(':"') + 2:-2]
    rd = re.compile('\[.*\]')
    hgtcont = re.search(rd, hgtcont).group()[2:-2]
    tl = hgtcont.split('","')
    # 这里还没整完
    open(dailyFile, 'at+').writelines(timestr + ',' + tl[0] + '\n')
    open(dailyFile, 'at+').write(timestr + ',' + tl[1] + '\n')


from base.httpclient import *
import time


def getSingleS(sid, market=None, type='p'):
    return sinaAPI(sid, market, type)


def collectDapanzhishu():
    dapandailyfile = 'd:/pySpace/AnalysisPython/data/dapanrishuju.csv'
    i = 0
    dpsid = [('000001', 'sh'), ('399001', 'sz'), ('399006', 'sz')]
    for sid, m in dpsid:
        open(dapandailyfile, 'at+').write(sinaAPI(sid, m, 's') + '\n')


def getStockBase(stockbase='../conf/stockbase.csv'):
    sb = tushare.get_stock_basics()
    if sb.index.size > 0:
        sb.to_csv(stockbase)


def getHistData(datapath):
    '''
    每天跑一次，捞取【sh,sz,cyb】的【5,15,30,60】
    datapath：数据存储位置
    存储在datapath，一个指数一个ktype一个文件
    :return:
    '''

    ktypes = ['5', '15', '30', '60']
    sids = ['sz', 'sh', 'cyb']

    for sid in sids:
        for ktype in ktypes:
            filename = os.path.join(datapath, sid + '_' + ktype + '.csv')
            if os.path.isfile(filename):
                # 有这个文件
                histtmp = pandas.read_csv(os.path.join(datapath, sid + '_' + ktype + '.csv'), index_col='date')
                start = datetime.datetime.strftime(
                    datetime.datetime.strptime(histtmp.index.max().split(' ')[0], DAYFORMAT) + timedelta(days=1),
                    DAYFORMAT)

                if start == datetime.datetime.strftime(datetime.datetime.now() + timedelta(days=1), DAYFORMAT):
                    # 今天数据已有
                    pass
                else:
                    tmp = tushare.get_hist_data(sid, ktype=ktype, start=start)
                    pandas.concat([tmp, histtmp]).to_csv(filename)
            else:
                # 没有这个文件
                tmp = tushare.get_hist_data(sid, ktype=ktype)
                tmp.to_csv(filename)