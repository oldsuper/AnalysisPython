__author__ = 'gaosongbo'
import ConfigParser


class PersonalException(Exception):
    pass


class baseT(object):
    def __init__(self, *args):
        # print 'base args', args
        if len(args) == 0:
            raise PersonalException('len(args) of baseT.__init__() is 0!')
        for item in args[0]:
            # print 'base __init__', item
            self.__setattr__(str(item[0]), item[1])

    def get(self, attrname):
        return self.__getattribute__(attrname)


class config_class(object):
    def __init__(self, configFile=None):
        conf = ConfigParser.ConfigParser()
        if configFile is None:
            conf.read('../conf/ana.properties')
        else:
            conf.read(configFile)
        for section in conf.sections():
            args = []
            for option in conf.options(section):
                args.append((option, conf.get(section, option)))
            self.__setattr__(section, baseT(args))

    def get(self, *args):
        print 'debug=========', len(args)
        # print 'get', args
        if len(args) == 0:
            raise PersonalException('No attribute name!')
        if len(args) != 2:
            raise PersonalException('attribute count must be 2!')
        if len(args) == 1:
            return self.__getattribute__(args[0]).attrname
        try:
            return self.__getattribute__(args[0]).get(args[1])
        except:
            raise PersonalException('plz check the attribute name', args)