#!/usr/bin/python
# coding=utf8
__author__ = 'gaosongbo'
import tushare
import pandas
import numpy
import datetime
from globalFactory import configFectory
from spider import todayDataSpider
import time
import threading
TIMEFORMAT='%Y%m%d%H%M%S'
import random
def test(name):
    st = random.Random.randint(1,20)
    print name,'sleep',st
    time.sleep()
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),name
def shouhu():
    c_threads = []
    cid = 1
    while(True):
        print "shouhu"
        if time.localtime().tm_sec % 10 == 0:
            cthread = threading.Thread(test,args=(str(cid)))
            print str(cid),'begin'
            cthread.run()
        cid+=1
        time.sleep(1)
class SHThread(threading.Thread):
    def __init__(self,thread_id,name):
        super(SHThread, self).__init__()  #调用父类的构造函数
        self.thread_id = thread_id
        self.name = name
    def run(self):
        print self.name,'starting...'
if __name__ == "__main__":
    # saomiao()
    # print configFectory.config()
    # todayDataSpider.saomiaoanhao()
    # todayDataSpider.hugutong()
    # import pandas
    # p=pandas.read_csv('D:\\pySpace\\AnalysisPython\\data/hgtDailyDetail.csv',index_col='timestr')
    # sched = BlockingScheduler()
    # sched.add_job(test, trigger='cron', second=5)
    # sched.start()
    # print todayDataSpider.collectDapanzhishu()

    shouhu = threading.Thread(target=shouhu)
    shouhu.run()