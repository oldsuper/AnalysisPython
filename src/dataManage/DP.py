# coding=utf8
__author__ = 'gaosongbo'

import os
import pandas
import tushare
import sys
import math
import numpy


def newstock(dpath):
    '''

    :param dpath:
    :return:
    '''
    dpl = []
    for fn in os.listdir(dpath):
        ffn = os.path.join(dpath, fn)
        sid = fn.split('.')[0]

        dpl.append(_kb(dpath, sid))
    return dpl


def _kb(dpath, sid, ds=20):
    t = pandas.read_csv(os.path.join(dpath, sid + '.csv'), index_col='date')
    t.sort_index(ascending=True, inplace=True)
    kbi = 0
    for i in range(t.index.size)[1:]:
        if t.iloc[i]['high'] != t.iloc[i]['low']:
            kbi = i
            break
    if kbi != 0:
        kbcp = t.iloc[kbi]['close']
        return unname(sid, t, kbcp, kbi, ds)
    return {'sid': sid, 'ld': 0, 'dr': 0, 'hd': 0, 'ur': 0}


def unname(sid, t, kbcp, kbi, ds):
    '''

    :param t:
    :param kbi:
    :param ds:
    :return:
        最低点出现在开板后第？天，下跌比例，最高点出现在最低点出现后的第？天，上涨比例
    '''
    k10 = t.iloc[kbi:kbi + ds]
    l10 = min(k10['low'])
    l10i = k10['low'].tolist().index(l10)
    h10 = max(k10.iloc[l10i:]['high'])
    h10i = k10.iloc[l10i:]['high'].tolist().index(h10)
    # return l10i, round((l10 / kbcp - 1) * 100, 2), h10i, round((h10 / l10 - 1) * 100, 2)
    return {'sid': sid, 'ld': l10i, 'dr': round((l10 / kbcp - 1) * 100, 2), 'hd': h10i,
            'ur': round((h10 / l10 - 1) * 100, 2)}


def newstockbuyandsell(dpath):
    '''
        计算收益

        买入策略：
            开板价格           bid=1
            开板收盘不涨停的    bid=2   不好计算，换成不以最高价收盘
            开板后第一天绿盘    bid=3
            开板后第一次低开    bid=4
            开板后跌破5日线     bid=5
            连续第二天绿盘，第二天买入   bind=6  没有这样的数据？！
        卖出策略：跌破5、10、20日线
    :param dpath:
    :return:
    '''
    dpl = []
    bidl = [1, 2, 3, 4, 5]
    slidl = [5, 10, 20]
    for fn in os.listdir(dpath):
        ffn = os.path.join(dpath, fn)
        sid = fn.split('.')[0]
        for bid in bidl:
            # 有卖策略的
            # for slid in slidl:
            # dpl.append(bs(dpath, sid, bid, slid))
            # 不给卖策略，计算最大可能收益，可以统计+5的概率，+10的概率
            # dpl.append(bs(dpath, sid, bid, slid=5, hp=True))
            # 不给卖策略，计算最大可能收益，可以统计+5的概率，+10的概率;hpc:hp控制按钮，为True时，统计开板到跌破5日线的最大值
            dpl.append(bs(dpath, sid, bid, slid=5, hp=True, hpc=True))
    return dpl


def bs(dpath, sid, bid=1, slid=5, hp=None, hpc=False):
    '''

    :param dpath:
    :param sid:
    :param bid:
    :param slid:
    :return:
        ic:收益
        bp:买入价格
        sp:卖出价格
        bd: 第？天买入
        sd：第？天卖出
        st：0，没有买入，1，买入，2，卖出
        hp:买入后的最高价格
        lp:买入后的最低价格
    '''
    t = pandas.read_csv(os.path.join(dpath, sid + '.csv'), index_col='date')
    t.sort_index(ascending=True, inplace=True)
    kbi = 0
    res = {'sid': sid, 'bid': bid, 'slid': slid, 'ic': 0, 'bp': 0, 'sp': 0, 'bd': 0, 'sd': 0, 'st': 0, 'hp': 0, 'lp': 0}
    for i in range(t.index.size)[1:]:
        if t.iloc[i]['high'] != t.iloc[i]['low']:
            kbi = i
            break
    if kbi != 0:
        kbcp = t.iloc[kbi]['close']
    else:
        return res
    if bid == 1:
        # 开板价格买入
        res['bp'] = t.iloc[kbi]['open']
        res['bd'] = kbi
        res['st'] += 1
    if bid == 2:
        # 开板后第一次不是最高价收盘
        for i in range(t.index.size)[kbi:]:
            if t.iloc[i]['close'] != t.iloc[i]['high']:
                res['bp'] = t.iloc[i]['close']
                res['bd'] = i
                res['st'] += 1
                break
    if bid == 3:
        for i in range(t.index.size)[kbi:]:
            if t.iloc[i]['p_change'] < 0:
                res['bp'] = t.iloc[i]['close']
                res['bd'] = i
                res['st'] += 1
                break
    if bid == 4:
        for i in range(t.index.size)[kbi:]:
            if t.iloc[i]['open'] < t.iloc[i - 1]['close']:
                res['bp'] = t.iloc[i]['open']
                res['bd'] = i
                res['st'] += 1
                break
    if bid == 5:
        for i in range(t.index.size)[kbi:]:
            if t.iloc[i]['close'] <= t.iloc[i]['ma5']:
                res['bp'] = t.iloc[i]['close']
                res['bd'] = i
                res['st'] += 1
                break
    if bid == 6:
        for i in range(t.index.size)[kbi:]:
            if t.iloc[i]['p_change'] < 0 and t.iloc[i + 1]['p_change'] < 0:
                res['bp'] = t.iloc[i + 1]['close']
                res['bd'] = i + 1
                res['st'] += 1
                break

    # 检查是否有买点，没有就返回
    if res['st'] == 0:
        return res
    if hp:
        if hpc:
            for i in range(t.index.size)[kbi:]:
                if t.iloc[i]['close'] <= t.iloc[i]['ma5']:
                    if i > res['bd']:
                        res['hp'] = max(t.iloc[res['bd']:i]['high'])
                        res['lp'] = min(t.iloc[res['bd']:i]['low'])
                        res['ic'] = round((res['hp'] / res['bp'] - 1) * 100, 2)
                        return res

        # 计算买入后的最高\低价格
        res['hp'] = max(t.iloc[res['bd']:]['high'])
        res['lp'] = min(t.iloc[res['bd']:]['low'])
        res['ic'] = round((res['hp'] / res['bp'] - 1) * 100, 2)
        return res

    else:
        # 进入卖点检查
        if slid == 5:
            sn = 'ma5'
        if slid == 10:
            sn = 'ma10'
        if slid == 20:
            sn = 'ma20'
        for i in range(t.index.size)[res['bd']:]:
            if t.iloc[i]['low'] <= t.iloc[i][sn]:
                # 收盘价卖出
                res['sp'] = t.iloc[i]['close']
                res['sd'] = i
                res['st'] += 1
                break
        #
        # 计算收益
        res['ic'] = round((res['sp'] / res['bp'] - 1) * 100, 2)
        return res


def dprisk(dpath, riskConfig):
    '''
    按照规则计算大盘指数的安全度
        1、格式化所有数据
            把大盘涨跌幅、交易量分成n等分，比如-2~-1：0，-1~0：1，。。。
        2、统计当日对应数字落在那个区间
        3、统计之前出现相应情况的概率
        4、定义一个初始的权重
        5、回归x次的权重，得到最接近实际情况的权重值
        6、使用5的权重，得到当前数据的安全指数
    第一步：
        1，2，3，6
    :param dpath:
    :return:
    '''
    print os.listdir(dpath)


def dpriskRefreshData(ffn):
    '''
    计算level,日线
    涨跌幅、交易量
    :param ffn:
    :return:
    '''
    p = pandas.read_csv(ffn,index_col='date')
    vnames = ['p_change', 'volume']
    for vname in vnames:
        vlist = p.get(vname)
        vLevelList = createMyDL(vlist.tolist())
        vLevelListName = vname + '_level'
        for i in p.index:
            p.loc[i][vLevelListName] = _getLevel(vLevelList, p.loc[i][vname], i)
    p.to_csv(ffn)
    # 计算当前涨跌幅第二天的概率
    lastIndex = p.index.max()



def _getLevel(vll, v, index=None):
    for i in range(len(vll)):
        try:
            if v >= vll[i][0] and v <= vll[i][1]:
                return i
        except:
            print "error", v, i, type(i), vll[i], type(index), index


def createMyDL(vl):
    '''
    获取诸如[1, 2, 4, 8, 16, 8, 4, 2, 1]的队列
    把极端情况列出来
    :param vl:
    :return:
    '''
    dl = []
    svl = vl
    vll = len(vl)
    svl.sort()
    fs = 9
    yz = 2
    tl = []
    for i in range(fs):
        tl.insert(i, int(math.pow(yz, (fs - 1) / 2 - math.fabs((fs - 1) / 2 - i))))
    print tl
    tt = sum(tl)
    ntl = []
    for i in range(fs):
        if i > 0:
            ntl.insert(i, tl[i] * 1.0 / sum(tl) + ntl[i - 1])
        else:
            ntl.insert(i, tl[i] * 1.0 / sum(tl))

    for i in range(fs):
        if i == fs - 1:
            tmp = svl[int(ntl[i - 1] * vll):]
        if i == 0:
            tmp = svl[:int(ntl[i] * vll)]
        if i > 0 and i < fs - 1:
            tmp = svl[int(ntl[i - 1] * vll):int(ntl[i] * vll)]
        # print tmp
        dl.insert(i, (min(tmp), max(tmp)))
    return dl