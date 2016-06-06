# coding = utf8
__author__ = 'gaosongbo'
import urllib
import re
import pandas
import time

CLS = ['gupiaoming', 'jinrikaipanjia', 'zuorishoupanjia', 'dangqianjia', 'jinrizuigaojia', 'jinrizuidijia',
       'jingbuyjia', 'jingsalejia', 'chengjiaogupiaoshu', 'chengjiaojine', 'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v',
       'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p', 's1_v', 's1_p', 's2_v', 's2_p', 's3_v', 's3_p', 's4_v', 's4_p', 's5_v',
       's5_p']
YEAR = time.strftime('%Y', time.localtime(time.time()))


def sinAPIGetConetent(url):
    try:
        content = urllib.urlopen(url).read()
        content = content.split('=')[1]
        content = content[1:-2]
        time = re.search(re.compile(YEAR+'-.*'), content).group()[:-3].replace(',', ' ')
        print content[:content.find(','+YEAR+'-')].split(',')
        print len(CLS)
        return pandas.DataFrame(content[:content.find(','+YEAR+'-')].split(','), index=CLS, columns=[time]).T
    except:
        return None


def sinaAPI(sid, m=None):
    baseURL = 'http://hq.sinajs.cn/list={sid}'
    if m != None:
        url = baseURL.replace('{sid}', m + sid)
    else:
        if sid.startswith('0') or sid.startswith('3'):
            url = baseURL.replace('{sid}', 'sz' + sid)
        if sid.startswith('6'):
            url = baseURL.replace('{sid}', 'sh' + sid)
    return sinAPIGetConetent(url)

# 399001
# 000001 sh sz
# 600570
# 300001