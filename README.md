目前处于代码初期后期会继续更新，欢迎师傅们加QQ提意见：NTYzMTY0NjE3 (防麦片)
# FofaSpider
fofa爬虫，支持高级查询语句批量获取域名和ip
### 依赖安装

pip install -r requirements.txt

### 使用方法

**Linux下使用**

python3 Spider.py '你的fofaCookie' -q 'domain="baidu.com"||title="百度"' -p 需要爬取的页数默认为5

**windows下使用不需要加引号，windows下的查询语句最好用 \ 转义一下（后面会想办法改）**

**同时windows的高级语法 || && 暂时不能使用后续会修改**

python3 Spider.py 你的fofaCookie  -q domain=\"baidu.com\" -p 需要爬取的页数默认为5

ps：普通用户高级语法查询只支持第一页，非高级语法搜索支持前5页，上面的例子是高级语法查询
