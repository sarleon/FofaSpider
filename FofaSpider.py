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
from urllib.parse import quote,unquote
from lxml import etree

# 生成一个txt的输出结果
def banner():
    print("""\033[36m
         _____      __       ____        _     _           
        |  ___|__  / _| __ _/ ___| _ __ (_) __| | ___ _ __ 
        | |_ / _ \| |_ / _` \___ \| '_ \| |/ _` |/ _ \ '__|
        |  _| (_) |  _| (_| |___) | |_) | | (_| |  __/ |   
        |_|  \___/|_|  \__,_|____/| .__/|_|\__,_|\___|_|
                                  |_|                   \033[0m                             
         # coded by KpLi0rn   website www.wjlshare.com
    """)

def Cmd():

    parser = optparse.OptionParser()
    parser.add_option('-q', '--query', dest='query', type=str, help='Your Fofa Query')
    parser.add_option('-r',dest='source',help='Your txt Path')   # 批量搜索文件
    parser.add_option('-p',dest='startpage',default=1,type=int,help='StartPage')
    parser.add_option('-s',dest='spidernum',default=0,type=int,help='Spider number')

    (options, args) = parser.parse_args()
    return options,args

class FofaSpider(object):

    def __init__(self,Cookie,Query,StartPage,SpiderNum):
        self.q = quote(Query)
        self.qbase64 = quote(str(base64.b64encode(Query.encode()),encoding='utf-8'))
        self.UserAgent = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16","Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0","Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
        # 这里的cookie 后面改成input 用户自己输入
        self.cookie = Cookie
        self.page = 1
        self.startpage = StartPage
        self.spidernum = SpiderNum
        self.dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.name = ("".join((self.dt.split(" ")[0]).split('-'))) + "_" + "".join((self.dt.split(" ")[1]).split(':'))

    def spider(self):

        global i
        i=0
        compile = re.compile('HTTP/1.1 (\d+) ')
        filename = xlwt.Workbook()
        sheet = filename.add_sheet('result')
        header = {
            "User-Agent": random.choice(self.UserAgent),
            "cookie": self.cookie
        }
        url = 'https://fofa.so/result?q={}&qbase64={}&full=true'.format(self.q, self.qbase64)
        html = requests.get(url=url, headers=header).text

        # pages = re.findall('<span clas="el-pagination__total">(\d*)</span>', html)
        try:
            nums =int("".join(re.findall('<span class="el-pagination__total">共 (.*) 条</span>',html)))
        except ValueError as e:
            nums = 1

        if nums < 10:
            page = 1
        else:
            page = nums//10+1

        print("\033[31m总共有{}页\033[0m".format(page))
        print("\033[31m查询语句为{}\033[0m".format(unquote(self.q,'utf-8')))
        try:
            pagenum = int(page) + 1
            for n in range(self.startpage,pagenum):
                if self.spidernum != 0 and (n == (self.startpage + self.spidernum +1)):
                    break
                target = 'https://fofa.so/result?page={}&page_size=10&qbase64={}&full=true'.format(n, self.qbase64)
                res = requests.get(url=target, headers=header).text
                if "0</span> 条匹配结果" in res:
                    sys.stdout.write("\033[31m0条匹配结果,请检查查询语句是否正确\n\033[0m")
                    sys.exit(0)

                if "error 500程序出错了" in res:
                    sys.stdout.write("\033[31m500程序出错了,请检查查询语句是否正确\n\033[0m")
                    sys.exit(0)

                if "游客使用高级语法只能显示第一页" in res:
                    sys.stdout.write('\033[31m游客使用高级语法只能显示第一页\n\033[0m')
                    sys.stdout.write(
                        '\033[31m搜集结果为{}.csv、\033[0m\033[31m\t{}.txt\n\n\033[0m'.format(spider.name, spider.name))
                    sys.exit(0)
                selector = etree.HTML(res)

                # //*[@id="__layout"]/div/div/div/div/div/div/div/div/div/div/div/div/div/span/text()
                # codes = "".join(selector.xpath('//*[@id="__layout"]/div/div/div/div/div/div/div/div/div/div/div/div/div/text()'))  # 爬取状态码
                codes = "".join(selector.xpath('//*[@id="__layout"]/div/div/div/div/div/div/div/div/div/div/div/div/div/span/text()'))  # 爬取状态码

                domain = selector.xpath('//*[@id="__layout"]/div/div/div/div/div/div/div/div/div/span/a/text()')  # 爬取域名或ip
                # domain_compile = re.compile("<a target=\"_blank\" href=\"(.*?)\"")
                # domain = domain_compile.findall(html)
                domain = [value.strip('\n').strip(' ') for value in domain if len(value.strip('\n').strip(' ')) != 0]
                nums = compile.findall(codes)  # 状态码列表


                # rdp等协议类查询
                if len(domain)==0:
                    scheme = selector.xpath('//*[@id="ajax_content"]/div/div[1]/div[1]/text()')
                    scheme = [value.strip(' ').strip('\n').strip(' ') for value in scheme]
                    print("\033[31m第%s页\033[0m" % str(n))
                    with open("{}.txt".format(self.name),"a+") as file:
                        for value in scheme:
                            print(value)
                            file.writelines(value)
                            file.writelines("\n")
                            sheet.write(i, 0, value)
                            i += 1
                    time.sleep(random.randint(5, 8))

                else:
                    # 域名和ip聚合成字典
                    res = zip(domain,nums)
                    print("\033[31m第%s页\033[0m" % str(n))
                    with open("{}.txt".format(self.name),"a+") as file:
                        for value in res:
                            file.writelines(value[0])
                            file.writelines("\n")
                            print(value[0] + ": " + value[1])
                            sheet.write(i, 0, value[0])
                            sheet.write(i, 1, value[1])
                            i += 1
                    time.sleep(random.randint(5,8))

                filename.save('./{}.csv'.format(self.name))
            sys.stdout.write('\033[31m搜集结果为{}.csv、\033[0m\033[31m\t{}.txt\n\n\033[0m'.format(spider.name, spider.name))


        except Exception as e:
            print("'\033[31m[!]异常退出！\033[0m'")
            print(e)


    def run(self):
        self.spider()

if __name__ == '__main__':
    banner()
    options, args = Cmd()
    cookie = "".join(args)

    try:
        if options.source is not None:
            with open(options.source,'r+',encoding='utf-8') as file:
                for value in file.readlines():
                    value = value.strip('\n')
                    try:
                        spider = FofaSpider(cookie, value, options.startpage, options.spidernum)
                        spider.run()
                    except:
                        pass
        else:
            spider = FofaSpider(cookie,options.query, options.startpage, options.spidernum)
            spider.run()

    except KeyboardInterrupt:
        print("\n\033[31m[!]用户退出\033[0m\n")
        sys.stdout.write('\033[31m搜集结果为{}.csv、\033[0m\033[31m\t{}.txt\n\n\033[0m'.format(spider.name,spider.name))
