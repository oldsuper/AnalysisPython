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
def test():
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# from apscheduler.schedulers import BlockingScheduler
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
    print todayDataSpider.collectDapanzhishu()