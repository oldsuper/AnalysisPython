# coding=utf8
__author__ = 'gaosongbo'


import os
import pandas


def weipan(datapath,zs=['sh'],ktypes=['15']):
    '''
    检查尾盘是否有抢筹，看十五分钟的
    :param datapath:
    :param zs:
    :param ktypes:
    :return:
    '''

    # for fn in os.listdir(datapath):
    #     if fn.find()
    # for id in zs:
    p = pandas.read_csv(os.path.join(datapath,'sh_15.csv'),index_col='date')




