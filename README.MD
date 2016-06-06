***
#概要
#设计
#模块
##API
##Data获取



|数据类型|数据源|粒度|存放路径|
|:-------|------|----|--------|
|大盘指数|tushare|日线、15分钟线||
|沪股通|东方财富|日线、15分钟|$ProjectRoot/data/hgtDailyDetail.csv|
|关注股|tushare|日线||

东方财富沪股通数据接口
http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=DPAB&sty=AHTZJL&js=({data:[(x)],time:%22(ut)%22})&cb=callback02446733516803452&callback=callback02446733516803452&_=1464757205199

##Trainer
##其他
###暗号模型
涨停收盘，买1、2、3、4、5的购买量比较奇怪（如11万，111，111，111，111这种）的