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
import math

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


class MyThread(threading.Thread):
    def __init__(self, target, *args):
        super(MyThread, self).__init__()  # 调用父类的构造函数
        self.target = target
        print args
        self.args = args

    def run(self):
        self.target(self.args[0], self.args[1])


def print_time(counter, s):
    while counter:
        print "counter = %d" % counter
        counter -= 1
        time.sleep(1)
    print s, 'is ok'


def show(s):
    time.sleep(random.randint(0, 10))
    print s, "close"


class JobThread(threading.Thread):
    def __init__(self, method, interval, begin, end):
        super(JobThread, self).__init__()  # 调用父类的构造函数
        self.threadname = method
        self.method = method
        self.interval = interval
        self.begin = begin
        index = self.method.rfind('.')
        package = self.method[:index]
        method = self.method[index + 1:]
        exec ("from " + package + " import " + method)
        self.target = eval(method)
        exec ("from " + self.method[:index] + " import " + self.method[index + 1:])
        today = datetime.datetime.now().strftime(DAYFORMAT)
        self.end = datetime.datetime.strptime(today + end, TIMEFORMAT)
        self.runtimes = []
        # +1秒的延迟
        nextrun = datetime.datetime.strptime(today + begin, TIMEFORMAT) + datetime.timedelta(seconds=1)

        while (nextrun <= self.end):
            self.runtimes.append(nextrun)
            nextrun = nextrun + datetime.timedelta(seconds=self.interval)

        self.nextruntime = None

    def run(self):
        # from spider.todayDataSpider import hugutong
        now = datetime.datetime.now()
        self.updateNextRunTime()

        while (self.nextruntime is not None):
            if self.nextruntime <= now:
                if math.pow((now - self.nextruntime).total_seconds(), 2) <= 1:
                    # print self.method, 'run ', ' at ', now
                    self.target()
                self.updateNextRunTime()
            else:
                sleeptime = (self.nextruntime - now).total_seconds()
                time.sleep(sleeptime)
                now = datetime.datetime.now()

    def updateNextRunTime(self):
        if self.nextruntime != None:
            index = self.runtimes.index(self.nextruntime)
            if len(self.runtimes) >= index + 2:
                self.nextruntime = self.runtimes[index + 1]
            else:
                self.nextruntime = None
        else:
            now = datetime.datetime.now()
            for nrt in self.runtimes:
                if nrt >= now:
                    self.nextruntime = nrt
                    break


def main():
    conf = configFectory.config()
    for section in conf.sections():
        if section.find('job') >= 0:
            # 定时任务
            print section
            print conf.items(section)


def testMethod(**args):
    print args


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

    # T1 = MyThread(eval('print_time'), 10, 'aaaaaa')
    # T2 = MyThread(print_time, 10, 'bbbbb')
    # T1.start()
    # T2.start()
    # T1.join()
    # T2.join()
    # main()
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

        # for jobThread in threads:
        # jobThread.join()
        # while (True):
        # print 'current_thread',threading.current_thread()
        # time.sleep(5)
        # jobThread.join()