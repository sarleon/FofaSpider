#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import time
import base64
import random
import optparse
import requests

from urllib.parse import quote
from lxml import etree
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

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
    parser.add_option('-p', '--page', dest='page', type='int', default=5, help='write the page you want crawel')
    parser.add_option('-q', '--query', dest='query', help='write the query you want')
    parser.add_option('-r',dest='source',help='you txt path')
    # parser.add_option('-c', '--cookie', dest='cookie', help='write your cookie')
    (options, args) = parser.parse_args()
    return options,args

class FofaSpider(object):

    # query 就是我们的查询语句
    def __init__(self,Cookie,query):
        self.q = quote(query)
        self.qbase64 = quote(str(base64.b64encode(query.encode()),encoding='utf-8'))
        # self.page = page
        self.s = requests.Session()
        self.ua = UserAgent()
        # 这里的cookie 后面改成input 用户自己输入
        self.header = {"User-Agent": self.ua.random,"Cookie": Cookie}
        self.domains = set()
        self.page = 1

    def spider(self):
        try:
            while(self.page):
                target = 'https://fofa.so/result?page={}&q={}&qbase64={}'.format(self.page,self.q, self.qbase64)
                res = self.s.get(url=target, headers=self.header).text
                # time.sleep(random.randint(7,10))
                selector = etree.HTML(res)
                domain = selector.xpath('//*[@id="ajax_content"]/div/div/div/a/text()')
                if len(domain) == 0:
                    print("爬取结束,或您的账号已无法再爬取")
                    break
                print("\033[31m第%s页\033[0m" % str(self.page))
                for value in domain:
                    value.strip(' ')
                    self.domains.add(value)
                    print(value)
                self.page+=1
                    # sys.exit(0)
                time.sleep(random.randint(3,7))

        except Exception as e:
            print(e)

    def run(self):
        self.spider()

if __name__ == '__main__':
    banner()
    options,args = cmd()
    cookie = "".join(args)
    # page = options.page + 1
    if options.source is not None:
        with open(options.source,'r+') as file:
            # cookie = "".join(args)
            for value in file.readlines():
                value = value.strip('\n')
                spider = FofaSpider( cookie, value)
                spider.run()
    else:
    # cookie = "".join(args)
        spider = FofaSpider(cookie,options.query)
        spider.run()

