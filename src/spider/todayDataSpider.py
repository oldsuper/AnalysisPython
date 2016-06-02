# coding=utf8
__author__ = 'gaosongbo'
# 仅按需求处理数据获取操作
# 沪股通
# 大盘数据：日、5分钟、15分钟、30分钟
# 个股数据：日、5分钟、15分钟、30分钟
import tushare
import pandas
import datetime
def saomiaoteshuguadan(sidfp = 'd:/\pySpace/AnalysisPython/conf/sids.csv'):

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
    #del df['name']
    df.to_csv('d:/pySpace/data/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_realtime_quotes.csv', encoding='gbk')
    print "get ok~"