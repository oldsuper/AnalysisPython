#!/usr/bin/python
# coding=utf8
__author__ = 'gaosongbo'
import tushare
import pandas
import numpy
import datetime
from globalFactory import configFectory
from spider import todayDataSpider



def saomiao():
    d = pandas.read_csv('D:/pySpace/data/2016-06-02_realtime_quotes.csv', index_col='code')
    print d[d['a1_v'] == numpy.nan].query('b2_v==b3_v').query('b2_v==b4_v').query('b2_v==b5_v')
    print datetime.datetime.now().strftime('%Y-%m-%d')


if __name__ == "__main__":
    # saomiao()
    # print configFectory.config()
    # todayDataSpider.saomiaoteshuguadan()
    saomiao()