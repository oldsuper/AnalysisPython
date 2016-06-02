__author__ = 'gaosongbo'
import ConfigParser
def config():
    conf=ConfigParser.ConfigParser()
    conf.read('../conf/ana.properties')
    return conf
