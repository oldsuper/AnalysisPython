#!/usr/bin/python
# coding=utf8
__author__ = 'gaosongbo'
# def init():
#     import ConfigParser
#     conf=ConfigParser.ConfigParser()
#     conf.read('../conf/ana.properties')
#     print conf.sections()

def saomiaoteshuguadan():
    sidfp='d:/codespace/AnalysisPython/conf/sids.csv'
    import tushare
    import pandas
    df = tushare.get_realtime_quotes('300312')
    i=0
    for l in open(sidfp).readlines():
        try:
            if len(l.strip())>0:
                sid = l.strip()
                sidd=tushare.get_realtime_quotes(sid)
                df=pandas.concat([df,sidd])
            if i>=100:
                print l.strip()
                i=0
            i+=1
        except Exception,e:
            print e,l.strip()
    #del df['name']
    df.to_csv('d:/data/20160601_realtime_quotes.csv',encoding='gbk')
    print "get ok~"
    
if __name__=="__main__":
    saomiaoteshuguadan()
