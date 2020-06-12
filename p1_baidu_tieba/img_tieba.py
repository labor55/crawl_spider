import requests
from lxml import etree
from time import sleep


class tieba():
        def __init__(self):
                self.headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"}
                self.url1 = "https://tieba.baidu.com/f?"
                self.url2 = "https://tieba.baidu.com"

        # 解析URL专用
        def parse_url(self,url):
                res = requests.get(url=url, headers=self.headers)
                return res

        # 负责解析网页，提取网页元素
        def load_page(self,text,xpath):
                html = etree.HTML(text)
                xpath_list = html.xpath(xpath)
                return xpath_list

        # 获取帖子内容的url列表，并调用函数保存
        def links_list(self, url):
                res = self.parse_url(url).text
                xpath = '//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]//a[@class="j_th_tit "]/@href'
                # 解析的是某吧的帖子详情页面
                links = self.load_page(res, xpath)
                l_list = []
                for i in links:
                        # 此路径拼接的是某吧的img图片页
                        link = self.url2 + i
                        l_list.append(link)

                # 对图片页面进行下载
                for link in l_list:
                        sleep(5)
                        self.img_write(link)


        # 解析图片地址，保存单个网页的图片文件
        def img_write(self, link):
                # 此xpath是查询某详情页面的img图片
                xpath = '//div[@class="l_post l_post_bright j_l_post clearfix  "]//img[@class="BDE_Image"]/@src'
                res = self.parse_url(link).text
                img_list = self.load_page(res, xpath)
                for i in img_list:
                        res = self.parse_url(i)
                        with open(f"./img/{i[-10:]}",'wb') as f:
                                f.write(res.content)
                                print(f'{i[-10:]}下载成功')

        # 主函数
        def main(self):
                name = input("输入你要进入的吧名(例如美女) >> ")
                start = input("请输入起始页码(0开始)>> ")
                end = input("请输入结束页码(一般为10页)>> ")
                # 输入格式化，
                if start.isdigit() and end.isdigit() and end>start:
                    for page in range(int(start),int(end)):
                            pn = (page-1) * 50
                            str1 = f'kw={name}&pn={pn}'
                            url = self.url1+str1
                            self.links_list(url)
                            print(f'页面{page}下载完成')
                else:
                    print("输入错误，请重新输入")
                    print("*"*60+"分隔符"+"*"*60+"\n")
                    return self.main()

if __name__ == '__main__':
        t = tieba()
        t.main()
