import requests
from lxml import etree
import csv
import re
from time import sleep
class baidu_search():
    '''
    入口：百度关键字
    返回百度搜索结果的标题和url，保存在csv文件中
    '''
    def __init__(self, keyword):
        self.keyword = keyword
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q\
            =0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
        }

    def writer_csv(self, url, writer):
        res = requests.get(url, headers=self.headers)
        html_str = etree.HTML(res.text)
        items = html_str.xpath('//*[@id="content_left"]/div/h3[@class="t"]')
        for item in items:
            arr = {}
            o_url = item.xpath('./a/@href')[0]
            arr['new_url'] = self.get_real(o_url)
            arr['title'] = item.xpath('string(./a)')
            writer.writerow(arr)
            print(arr['title'])
        sleep(1)
        return res

    def get_next_url(self, res):
        next = re.findall('>10<\/span><\/a><a href="(\/s\?wd=.*?rsv_page=1)" class="n">下一页', res.text)
        if next:
            next_url = "https://www.baidu.com" + next[0]
            return next_url
        return None

    def get_real(self, o_url):
        '''获取重定向url指向的网址'''
        r = requests.get(o_url, allow_redirects=False)  # 禁止自动跳转
        if r.status_code == 302:
            try:
                return r.headers['location']  # 返回指向的地址
            except:
                pass
        return o_url  # 返回源地址

    def main(self):
        flag = True
        url = "https://www.baidu.com/s?ie=UTF-8&wd=" + self.keyword
        with open(f"{self.keyword}12.csv", "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["title", "new_url"])
            writer.writeheader()
            res = self.writer_csv(url, writer)
            next_url = self.get_next_url(res)
            while flag:
                res = self.writer_csv(next_url, writer)
                next_url = self.get_next_url(res)
                if not next_url:
                    flag = False

if __name__ == '__main__':
    keyword = '石油网站'
    b = baidu_search(keyword=keyword)
    b.main()
