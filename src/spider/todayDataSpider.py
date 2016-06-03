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

PROJECTPATH = 'd:/\pySpace/AnalysisPython/'


def getToday():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def saomiaoanhao(dataFilepath):
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
    today = getToday()
    hgtcont = re.search(r, content).group()
    open(dateBackupFile, 'at+').write(hgtcont + '\n')
    rd = re.compile('[.*]')
    hgtcont = re.search(rd, hgtcont).group()
    tl = hgtcont.split('","')
    # 这里还没整完
    open(dailyFile, 'at+').write(hgtcont + '\n')

