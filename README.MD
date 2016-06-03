***
#概要
#设计
#模块
##API
##Data获取

###SH
大盘指数，主要是三大板块
###HGT
通过东方财富的接口获取HGT买卖数据
####地址
http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=DPAB&sty=AHTZJL&js=({data:[(x)],time:%22(ut)%22})&cb=callback02446733516803452&callback=callback02446733516803452&_=1464757205199
####数据存放
$ProjectRoot/data/hgtHistory.csv
####记录粒度
日，15分钟



|数据类型|数据源|粒度|存放路径|
|:-------|------|----|--------|
|大盘指数|tushare|日线、15分钟线|tushare|
|:-------|------|----|--------|
|沪股通|http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=DPAB&sty=AHTZJL&js=({data:[(x)],time:%22(ut)%22})&cb=callback02446733516803452&callback=callback02446733516803452&_=1464757205199|日线、15分钟|$ProjectRoot/data/hgtHistory.csv|
|:-------|------|----|--------|
|关注股|tushare|日线|略|
|:-------|------|----|--------|
|||||
|:-------|------|----|--------|

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell


##Trainer
##其他
###暗号模型
涨停收盘，买1、2、3、4、5的购买量比较奇怪（如11万，111，111，111，111这种）的