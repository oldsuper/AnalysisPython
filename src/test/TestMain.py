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
