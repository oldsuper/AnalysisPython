#!/usr/bin/python
# coding=utf8
__author__ = 'gaosongbo'
import tushare
import pandas
import numpy
import datetime
from globalFactory import configFectory
from spider.todayDataSpider import *
from spider.historyData import *
from dataManage.DP import *
import time
import threading
import math
from base.jobThread import JobThread

TIMEFORMAT = '%Y%m%d%H%M%S'
DAYFORMAT = '%Y%m%d'
import random


def test(name):
    st = random.Random.randint(1, 20)
    print name, 'sleep', st
    time.sleep()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), name


def shouhu():
    c_threads = []
    cid = 1
    while (True):
        print "shouhu"
        if time.localtime().tm_sec % 10 == 0:
            cthread = threading.Thread(test, args=(str(cid)))
            print str(cid), 'begin'
            cthread.run()
        cid += 1
        time.sleep(1)


def testMethod(**args):
    print args


def useThread():
    threads = []
    conf = configFectory.config()
    for section in conf.sections():
        if section.find('job') >= 0:
            jobThread = JobThread(conf.get(section, 'method'), conf.getint(section, 'interval'),
                                  conf.get(section, 'begin'), conf.get(section, 'end'))
            # print jobThread.runtimes
            for i in jobThread.runtimes:
                print jobThread.method, i.strftime(TIMEFORMAT)
            threads.append(jobThread)
    print len(threads)
    for jobThread in threads:
        jobThread.start()
        jobThread.join()


def main():
    conf = configFectory.config()
    # print nsb
    # getHistoryData('d:/', '600570', start='2003-12-16', end='2016-07-07')
    # getHistData('D:/pycode/data/dp/')
    dpath = 'D:/pycode/data/nsb/'
    confpath = 'D:/pycode/AnalysisPython/conf/'

    # 获取stockbasic数据，存储
    # fetchStockBase(confpath)

    # nsb = getNewStock(conf.get('dataConfig','stockbase'))

    # 计算新股的某些数据
    # rs = newstock(dpath)
    # prs = pandas.DataFrame(rs).to_csv('D:/pycode/data/ana/nsb.csv')


    # 计算新股的买卖点策略
    # rs = newstockbuyandsell(dpath)
    # pandas.DataFrame(rs).to_csv('D:/pycode/data/ana/newstockbuyandsell_hpc.csv')

    # 获取大盘数据
    # DP('D:/pycode/data/dp',dps=['sh'], ktypes=['D'])
    DP('D:/pycode/data/dp')


if __name__ == "__main__":
    # saomiao()
    # print configFectory.config()
    # todayDataSpider.anhaomoxing()
    # todayDataSpider.hugutong()
    # import pandas
    # p=pandas.read_csv('D:\\pySpace\\AnalysisPython\\data/hgtDailyDetail.csv',index_col='timestr')
    # sched = BlockingScheduler()
    # sched.add_job(test, trigger='cron', second=5)
    # sched.start()
    # print todayDataSpider.collectDapanzhishu()

    # testMethod(a=1, b=2, c=[1, 2, 3])

    # t = (datetime.datetime.strptime('20160622' + '175200', TIMEFORMAT))
    # print t
    # t = t + datetime.timedelta(seconds=30)
    # print t
    # print datetime.datetime.now()
    # print type(t)
    # td = datetime.datetime.now() - t
    # print td
    # print td.total_seconds()

    # 使用thread运行任务 demo
    # useThread()


    # 获取当前stockbase数据
    # todayDataSpider.getStockBase()
    main()