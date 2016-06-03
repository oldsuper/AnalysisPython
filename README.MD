***
#概要
#设计
#模块
##API
##Data获取



|数据类型|数据源|粒度|存放路径|地址|
|大盘指数|tushare|日线、15分钟线|tushare||
|沪股通|沪股通|日线、15分钟|$ProjectRoot/data/hgtHistory.csv|http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=DPAB&sty=AHTZJL&js=({data:[(x)],time:%22(ut)%22})&cb=callback02446733516803452&callback=callback02446733516803452&_=1464757205199|
|关注股|tushare|日线|略||



##Trainer
##其他
###暗号模型
涨停收盘，买1、2、3、4、5的购买量比较奇怪（如11万，111，111，111，111这种）的