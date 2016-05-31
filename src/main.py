#!/usr/bin/python
# coding=utf8
__author__ = 'gaosongbo'
def init():
    import ConfigParser
    conf=ConfigParser.ConfigParser()
    conf.read('../conf/ana.properties')
    print conf.sections()
if __name__=="__main__":
    init()