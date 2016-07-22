__author__ = 'gaosongbo'
import ConfigParser
def config(configFile=None):
    conf=ConfigParser.ConfigParser()
    if configFile==None:
        conf.read('../conf/ana.properties')
    else:
        conf.read(configFile)
    return conf