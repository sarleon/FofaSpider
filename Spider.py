# !/usr/bin/env python
# coding: utf-8

import time
import base64
import random
import optparse
import requests

from datetime import datetime
from urllib.parse import quote
from lxml import etree

def banner():
    print("""\033[36m
         _____      __       ____        _     _           
        |  ___|__  / _| __ _/ ___| _ __ (_) __| | ___ _ __ 
        | |_ / _ \| |_ / _` \___ \| '_ \| |/ _` |/ _ \ '__|
        |  _| (_) |  _| (_| |___) | |_) | | (_| |  __/ |   
        |_|  \___/|_|  \__,_|____/| .__/|_|\__,_|\___|_|
                                  |_|                   \033[0m                             
         # coded by KpLi0rn   website www.wjlshare.xyz
    """)



def cmd():
    parser = optparse.OptionParser()
    parser.add_option('-q', '--query', dest='query', help='write the query you want')
    parser.add_option('-r',dest='source',help='you txt path')   # 批量搜索文件
    # parser.add_option('-o',dest='output',default='')
    # parser.add_option('-c', '--cookie', dest='cookie', help='write your cookie')
    (options, args) = parser.parse_args()
    return options,args

class FofaSpider(object):

    # query 就是我们的查询语句
    def __init__(self,Cookie,query):
        self.q = quote(query)
        self.qbase64 = quote(str(base64.b64encode(query.encode()),encoding='utf-8'))
        self.s = requests.Session()
        self.UserAgent = ["Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)", "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)","Baiduspider-image+(+http://www.baidu.com/search/spider.htm)","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)","360spider (http://webscan.360.cn)","Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)","Googlebot-Image/1.0","Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)","Sosospider+(+http://help.soso.com/webspider.htm)","Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0","Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
        # 这里的cookie 后面改成input 用户自己输入
        self.Cookie = Cookie
        self.domains = set()
        self.page = 1

    def spider(self):

        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dt1 = "".join((dt.split(" ")[0]).split('-'))
        dt2 = "".join((dt.split(" ")[1]).split(':'))
        name = dt1 + "_" + dt2

        header = {"User-Agent": random.choice(self.UserAgent), "Cookie": self.Cookie}
        try:
            while(self.page):
                target = 'https://fofa.so/result?page={}&q={}&qbase64={}'.format(self.page,self.q, self.qbase64)
                res = self.s.get(url=target, headers=header).text
                selector = etree.HTML(res)
                domain = selector.xpath('//*[@id="ajax_content"]/div/div/div/a/text()')
                if len(domain) == 0:
                    print("\033[31m[!]爬取结束,或您的账号已无法再爬取\033[0m")
                    break

                print("\033[31m第%s页\033[0m" % str(self.page))
                for value in domain:
                    value.strip(' ')
                    self.domains.add(value)
                    print(value)
                    with open('{}.txt'.format(name),'a+') as file:
                        file.writelines(value)
                        file.write('\n')
                self.page+=1
                time.sleep(random.randint(5,8))

            print('\033[31m[+]结果输出在{}.txt中\033[0m'.format(name))

        except Exception as e:
            print('\033[31m[+]结果输出在{}.txt中\033[0m'.format(name))
            print("'\033[31m[!]异常退出！\033[0m'")

    def run(self):
        self.spider()

if __name__ == '__main__':
    banner()
    options, args = cmd()
    cookie = "".join(args)
    try:
        if options.source is not None:
            with open(options.source,'r+') as file:
                # cookie = "".join(args)
                for value in file.readlines():
                    value = value.strip('\n')
                    spider = FofaSpider(cookie, value)
                    spider.run()
        else:
            spider = FofaSpider(cookie,options.query)
            spider.run()

    except Exception as e:
        print("'\033[31m[!]异常退出！\033[0m'")


