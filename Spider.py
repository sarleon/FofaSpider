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
    # if options.query is None or options.cookie is None:
    # if options.query is None:
    #     parser.print_help()
    #     sys.exit(0)
    # else:
    return options,args

class FofaSpider(object):

    # query 就是我们的查询语句
    def __init__(self,page,Cookie,query):
        self.q = quote(query)
        self.qbase64 = quote(str(base64.b64encode(query.encode()),encoding='utf-8'))
        self.page = page
        self.s = requests.Session()
        self.ua = UserAgent()
        # 这里的cookie 后面改成input 用户自己输入
        self.header = {"User-Agent": self.ua.random,"Cookie": Cookie}
        self.domains = set()

    def spider(self,page):
        try:
            target = 'https://fofa.so/result?page={}&q={}&qbase64={}'.format(page,self.q, self.qbase64)
            res = self.s.get(url=target, headers=self.header).text
            selector = etree.HTML(res)
            domain = selector.xpath('//*[@id="ajax_content"]/div/div/div/a/text()')
            for value in domain:
                value.strip(' ')
                self.domains.add(value)
                print(value)
            time.sleep(random.randint(3,7))
        except Exception as e:
            print(e)

    def run(self):
        pool = ThreadPoolExecutor(2)
        [pool.submit(self.spider,i) for i in range(1,self.page)]


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
                spider = FofaSpider(options.page + 1, cookie, value)
                spider.run()
    else:
    # cookie = "".join(args)
        spider = FofaSpider(options.page+1,cookie,options.query)
        spider.run()

