__author__ = 'gaosongbo'


def miyan():
    juzhen = [[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 16]]
    juzhenjiagong = []
    for line in juzhen:
        juzhenjiagong.append([])
        index = juzhen.index(line)
        for item in line:
            juzhenjiagong[index].append([item, 0])

    # begin = 0
    # step = 90
    # max = 360
    fx = 0

    i = 0
    j = 0
    print juzhenjiagong[i][j][0]
    juzhenjiagong[i][j][1] = 1
    while (end(juzhenjiagong) == False):
        x, fx, i, j = next(juzhenjiagong, fx, i, j)
        juzhenjiagong[i][j][1] = 1
        print x
        # time.sleep(0.05)


def getfx(fx, ci, cj):
    begin = 0
    step = 90
    max = 270
    if fx == 360:
        fx = 0
    if fx == 0:
        tj = cj + 1
        ti = ci
    if fx == 90:
        tj = cj
        ti = ci + 1
    if fx == 180:
        tj = cj - 1
        ti = ci
        if tj < 0:
            return getfx(fx + 90, ci, cj)
    if fx == 270:
        tj = cj
        ti = ci - 1
        if ti < 0:
            return getfx(fx + 90, ci, cj)
    return fx, ti, tj


def next(jz, fx, ci, cj):
    fx, ti, tj = getfx(fx, ci, cj)
    try:
        if jz[ti][tj][1] == 0:
            return jz[ti][tj][0], fx, ti, tj
        else:
            fx, ti, tj = getfx(fx + 90, ci, cj)
            if jz[ti][tj][1] == 0:
                return jz[ti][tj][0], fx, ti, tj
            else:
                return None, 0, 0, 0
    except:
        fx = fx + 90
        return next(jz, fx, ci, cj)


def end(jz):
    res = True
    for l in jz:
        for i in l:
            res = res and (i[1] == 1)
    return res


def testargs(*args, **kwargs):
    print args
    print kwargs


import types


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


class PersonalException(Exception):
    pass


class T(object):
    a = 1
    b = ['a', 'b']
    c = {1: 'a'}

    def __init__(self, *args, **kwargs):
        # if args is not None:
        # print 'args', args
        # if kwargs is not None:
        # print 'kwargs', kwargs
        for k in kwargs:
            if isinstance(kwargs[k], dict):
                # print 'setattr', tuple(kwargs[k].items())
                baset = baseT(tuple(kwargs[k].items()))
                self.__setattr__(k, baset)
            else:
                self.__setattr__(k, kwargs[k])

    def get(self, *args):
        # print 'get', args
        if len(args) == 0:
            raise PersonalException('No attribute name!')
        if len(args) > 2:
            raise PersonalException('attribute list limit is 2!')
        try:
            if len(args) == 1:
                return self.__getattribute__(args[0])
            return self.__getattribute__(args[0]).get(args[1])
        except:
            raise PersonalException('plz check the attribute name', args)


# # testargs(1, 2, 3, 4, a=1, xx={1, 2, 3})
# t = T(a={'x': 'a1', 'y': 'a2'}, b='aaaaaaaa')
# # print '===', t.get('a', 'z')
# print '===', t.a.x
# print '===', t.b.z
import random


def get_history_statics(x):
    limit = 5
    res = [
        [.2, .2, .4, .1, .1],
        [.2, .3, .1, .2, .2],
        [.1, .1, .3, .3, .2],
        [.6, .1, .1, .1, .1],
        [.1, .5, .1, .2, .1]
    ]
    if x > 0:
        return res
    return [res[1], res[2], res[3], res[4], res[0]]


def main(a, b):
    limit = 5
    wl = [1.2, .7]
    h = {0: get_history_statics(1),
         1: get_history_statics(0)}
    res = []
    for i in range(limit):
        r1 = [x * wl[0] for x in h[0][a]]
        r2 = [x * wl[1] for x in h[1][b]]
    res = [r1[i] + r2[i] for i in range(len(r1))]
    s = sum(res)
    for i in range(len(res)):
        res[i] = round(res[i] * 1.0 / s, 2)
    return res


if __name__ == "__main__":
    print main(2, 2)