import requests
import time
from lxml import etree
from multiprocessing import pool
import pymongo

class biqukan():

    def __init__(self):
        self.url = "https://www.biqukan.com"
        # 网址 + 小说名
        self.url2 = self.url + '/1_1094/'
        self.headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}

    # 域名解析
    def get_page(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res

    # 获取目录---返回章节目录网址
    def mulu(self):
        xpath = '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href'
        res = self.get_page(self.url2)
        html = etree.HTML(res.text)
        con = html.xpath(xpath)
        return con

    # 写入文件
    def detail(self, con, collect):
        for url in con[4:14]:
            # 网址拼接
            url_con = self.url + url
            res = self.get_page(url_con)
            html = etree.HTML(res.text)
            title = html.xpath('//*[@id="content"]/../h1/text()')[0]
            content = html.xpath('//*[@id="content"]')[0].xpath('string(.)')
            content.replace(', ','').replace('[','').replace(']','')
            collect.insert_one({title:content})
            print(f'{title} 成功 ')
            time.sleep(1)

    def main(self):
        mon = pymongo.MongoClient()
        collect = mon.test2.bqk1
        con = self.mulu()
        self.detail(con, collect)

if __name__ == '__main__':
    b = biqukan()
    b.main()
