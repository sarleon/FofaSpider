# !/usr/bin/env python
# coding: utf-8

import sys
import re
import time
import xlwt
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
    parser.add_option('-p',dest='startpage',default=1,type=int,help='input the StartPage')
    parser.add_option('-s',dest='spidernum',default=0,type=int,help='intput the Spider number')
    (options, args) = parser.parse_args()
    return options,args

class FofaSpider(object):

    # query 就是我们的查询语句
    def __init__(self,Cookie,query,startpage,spidernum):
        self.q = quote(query)
        self.qbase64 = quote(str(base64.b64encode(query.encode()),encoding='utf-8'))
        self.UserAgent = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16","Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0","Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
        # 这里的cookie 后面改成input 用户自己输入
        self.Cookie = Cookie
        self.page = 1
        self.startpage = startpage
        self.spidernum = spidernum


    def spider(self):
        global i
        i=0
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dt1 = "".join((dt.split(" ")[0]).split('-'))
        dt2 = "".join((dt.split(" ")[1]).split(':'))
        name = dt1 + "_" + dt2
        # 提取状态码
        compile = re.compile('HTTP/1.1 (\d+) ')
        filename = xlwt.Workbook()
        sheet = filename.add_sheet('result')
        header = {"User-Agent": random.choice(self.UserAgent), "Cookie": self.Cookie}
        url = 'https://fofa.so/result?q={}&qbase64={}&full=true'.format(self.q, self.qbase64)
        html = requests.get(url=url, headers=header).text
        # print(html)
        pages = re.findall('>(\d*)</a> <a class="next_page" rel="next"', html)
        if len(pages) == 0:
            page = 1
        else:
            page = pages[0]

        print("\033[31m总共有{}页\033[0m".format(page))
        print("\033[31m查询语句为{}\033[0m".format(self.q))
        try:
            pagenum = int(page) + 1
            for n in range(self.startpage,pagenum):
                if self.spidernum != 0 and (n == (self.startpage + self.spidernum +1)):
                    break

                target = 'https://fofa.so/result?page={}&q={}&qbase64={}&full=true'.format(n, self.q, self.qbase64)
                res = requests.get(url=target, headers=header).text
                selector = etree.HTML(res)
                codes = "".join(selector.xpath('//*[@id="ajax_content"]/div/div[2]/div[2]/div/div[1]/text()'))  # 爬取状态码
                domain = selector.xpath('//*[@id="ajax_content"]/div/div[1]/div[1]/a/text()')  # 爬取域名或ip
                domain = [value.strip('\n').strip(' ') for value in domain if len(value.strip('\n').strip(' ')) != 0]
                nums = compile.findall(codes)  # 状态码列表
                # res = zip(domain, nums)
                if len(domain) == 0:
                    sys.exit(0)
                # rdp等协议类查询
                if len(domain)==0:
                    domain = selector.xpath('//*[@id="ajax_content"]/div/div/div[1]/div[1]/text()')
                    domain = [value.strip(' ').strip('\n').strip(' ') for value in domain]
                    print("\033[31m第%s页\033[0m" % str(n))
                    for value in domain:
                        print(value)
                        sheet.write(i, 0, value)
                        i += 1
                    time.sleep(random.randint(5, 8))

                else:
                    # 域名和ip聚合成字典
                    res = zip(domain,nums)
                    print("\033[31m第%s页\033[0m" % str(n))
                    for value in res:
                        print(str(i) +": " +value[0] + ": " + value[1])
                        sheet.write(i, 0, value[0])
                        sheet.write(i, 1, value[1])
                        i += 1
                    time.sleep(random.randint(5,8))

                filename.save('./{}.csv'.format(name))
            sys.stdout.write('\033[31m搜集结果为{}.csv\n\n\033[0m'.format(name))

        except Exception as e:
            print("'\033[31m[!]异常退出！\033[0m'")
            print(e)

    def run(self):
        self.spider()

if __name__ == '__main__':
    banner()
    options, args = cmd()
    cookie = "".join(args)

    try:
        if options.source is not None:
            with open(options.source,'r+',encoding='utf-8') as file:
                for value in file.readlines():
                    value = value.strip('\n')
                    spider = FofaSpider(cookie, value, options.startpage, options.spidernum)
                    spider.run()
        else:
            spider = FofaSpider(cookie,options.query, options.startpage, options.spidernum)
            spider.run()

    except Exception as e:
        print("'\033[31m[!]异常退出！\033[0m'")
        print(e)

