目前处于代码初期后期会继续更新，欢迎师傅们加QQ提意见：NTYzMTY0NjE3 (防麦片)

# 待处理问题
发现爬取一些rdp协议等结果会出现异常并且此类没有状态码，会尽快解决

# FofaSpider

本脚本基于python3开发

支持批量爬取功能，将语句写在txt中会进行批量查询(为了防止被ban，爬取周期有可能较长)

支持输出爬取结果到excel中，结果和状态码一一对应

为了防止爬取过程中被ban延长了time.sleep()的时间，平均sleep 6秒左右

## 声明

请不要利用本工具从事一切和违法有关的事情，如使用本工具则默认同意

## 依赖安装

pip install -r requirements.txt

## 项目更新

项目增加新的库 xlwt 更新的时候重新安装一下依赖

`git pull`

**ps：普通用户高级语法查询只支持第一页，非高级语法搜索支持前5页，会员账号一天只能爬取1w条数据**

## Linux下使用

`python3 Spider.py '你的fofaCookie' -q 'domain="baidu.com"||title="百度"' `

## Windows下使用

windows用户强烈推荐在cmder中使用，在cmd中使用没有高亮

**windows下使用不需要加引号**

同时windows的高级语法中的|| && 只能在 -r 读取txt文本的模式下使用

`python3 Spider.py 你的fofaCookie  -q domain="baidu.com" `

ps:windows使用过程中如果出现没结果的情况有可能是输入引号但是由于一些终端问题导致引号没有带入查询语句

解决方案：将查询语句写入txt文本 利用 -r 模式来读取数据(此bug后续会尝试解决)

## 支持批量查询语句
将查询语句写在txt文档中，一个语句换一行，格式如下:

domain="baidu.com"

domain="bilibili.com"

**Linux下**
`python3 Spider.py -r 你文本的路径 'cookie'`

**Windows下**
`python3 Spider.py -r 你文本的路径 cookie`

## 更新日志：
05.13 新增输出结果到文本功能,取消了fakeUseragent的使用

05.14 新增部分代码高亮,以及结果判断

05.18 修改了输出文件名的格式，取消了md5对文件名加密命名方式，将文件名改成时间方式，
      删去了部分多余结构，爬取过程中用户中断也会将之前爬取的信息写入txt中
      
05.20 修改了部分逻辑添加报错文本机制

05.21 修改了部分小bug

05.22 大改，使用了xlwt库需要进行依赖安装，输出中会显示状态码，输出结果改成excel表格(csv格式)，在爬取过程中会同时爬取fofa的状态码，test.py为原来的代码,修改了爬取不全的bug,循环改成for循环


