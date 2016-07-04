#!/usr/bin/python
# coding=utf8
__author__ = 'gaosongbo'

import time
import threading
import random
import datetime
import math

TIMEFORMAT = '%Y%m%d%H%M%S'
DAYFORMAT = '%Y%m%d'

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