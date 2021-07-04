# FofaSpider


本脚本基于python3开发，支持批量爬取功能，将语句写在txt中会进行批量查询

excel版会自动爬取信息同时输出到excel、txt中 (由于爬取的是fofa中的状态码，所以有可能会出现状态码实际情况不吻合的情况)

可自定义从第几页进行爬取,爬取几页

为了防止爬取过程中被ban延长了time.sleep()的时间，平均sleep 6秒左右

## 免责声明

依据中华人民共和国网络安全法第二十七条：任何个人和组织不得从事非法侵入他人网络、干扰他人网络正常功能、窃取网络数据等危害网络安全的活动；不得提供专门用于侵入网络、干扰网络正常功能及防护措施、窃取网络数据等危害网络安全活动的程序、工具；明知他人从事危害网络安全的活动的不得为其提供技术支持、广告推广、支付结算等帮助。

使用本工具则默认遵守网络安全法

## 依赖安装

pip install -r requirements.txt

## 项目更新

`git pull`

**ps：普通用户高级语法查询只支持第一页，非高级语法搜索支持前5页，会员账号一天只能爬取1w条数据**

# 使用说明



## Linux

`python3 Spider.py 'Cookie' -q 'domain="baidu.com"||title="百度"' `

-p 参数可自定义从第几页开始爬取，可不加不加 -p 参数则默认为1 -s 爬取几页(该参数可不加)

`python3 Spider.py 'Cookie' -q 'domain="baidu.com"' -p 5 -s 10`

## Windows

windows下强烈推荐在powershell中运行
`python3 Spider.py 'Cookie' -q 'domain="baidu.com"||title="百度"' `


## 支持批量查询语句
将查询语句写在txt文档中，一个语句换一行，格式如下:

domain="baidu.com"

domain="bilibili.com"

**Linux下**
`python3 Spider.py -r 你文本的路径 'Cookie'`

**Windows下**
`python3 Spider.py -r 你文本的路径 Cookie`



