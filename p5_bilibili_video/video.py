'''
本代码地址为：https://github.com/labor55/bilibili_video_spider
参考于Mike_Shine(一时没有找到他的地址)，在此基础上修改和改进

# 程序说明：
输入up主id，就可以获取他/她的投稿视频（没有翻页，可以自行加），投稿的分集也会下载
由于没有登录，故下载的清晰度比较低,也不可以选清晰度。(b站登录验证码更新了，暂时没有破解)
简单的进度条

跟新于2019-07-26，作者：labor55(https://github.com/labor55)
欢迎来看看，不足之处，请指正
'''
import requests
import json
from parse import parse_url
from time import sleep
import re
import os
import datetime
from lxml import etree
import warnings
from progressbar import ProgressBar
# 忽视警告
warnings.filterwarnings("ignore")

def get_proxies():
    '''获取代理ip'''
    proxy = parse_url('http://127.0.0.1:5010/get/')
    if proxy:
        proxies = {'http':'http://'+proxy}
        print(f'使用的代理ip地址为：{proxies["http"]}')
    else:
        proxies = None
    return proxies

def get_response(User_Mid):
    '''
    函数描述：获取用户主页视频列表
    入口参数：用户b站id
    出口参数：视频列表（视频aid，用户名，视频标题）
    '''
    # ajax请求 前面要加上主机地址!在这里就是space.xxxxxx,获取的是用户主页信息
    url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid='+ str(User_Mid)+'&pagesize=100&tid=0&page=1&keyword=&order=pubdate'
    headers = {
        'Host': 'space.bilibili.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Referer': 'https://space.bilibili.com/' + str(User_Mid)+ '/',    # 这里是Mid
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    # 代理获取，可以不用代理
    proxies = get_proxies()

    # 返回的是json数据
    res = requests.get(url=url, headers=headers, verify=False, proxies=proxies)
    res = json.loads(res.text)
    v_count = res['data']['count']
    v_count = v_count if v_count<=100 else 100  #最大的请求size是100
    video_List=[]
    for num in range(v_count):
        aid =  res['data']['vlist'][num]['aid']
        title = res['data']['vlist'][num]['title']
        author = res['data']['vlist'][num]['author']
        tmp = {"aid":aid,"title":title,"author":author}
        video_List.append(tmp)
    return video_List


def sub(s):
    '''为了替换掉命名时的非法字符，不然下载创建路径时会报错'''
    patn_1 = re.compile(r'\?')
    patn_2 = re.compile(r'\/')
    patn_3 = re.compile(r'\\')
    patn_4 = re.compile(r'\|')
    patn_5 = re.compile(r'\:')
    patn_6 = re.compile(r'\<')
    patn_7 = re.compile(r'\>')
    patn_8 = re.compile(r'\*')
    patn_9 = re.compile(r'\:')

    s = re.sub(patn_1,"",s)
    s = re.sub(patn_2,"",s)
    s = re.sub(patn_3,"",s)
    s = re.sub(patn_4,"",s)
    s = re.sub(patn_5,"",s)
    s = re.sub(patn_6,"",s)
    s = re.sub(patn_7,"",s)
    s = re.sub(patn_8,"",s)
    s = re.sub(patn_9,"",s)
    return s

def parse_download_url(aid):
    '''
    函数功能：解析视频地址
    入口参数：视频aid
    出口参数：视频地址列表
    '''
    # 这里只下载一集，若是有多集，可以在url加参数?p=num
    # 首页地址
    url = 'https://www.bilibili.com/video/av'+ str(aid)
    # 源码下载，并用正则解析出视频地址
    url_lists = []
    html_str = parse_url(url)
    url_patn = re.compile("video_url: '(.*?)',")
    # 第一集加入list
    try:
        v_url = re.findall(url_patn, html_str)[0]
    except:
        return
    v_url = 'http:'+v_url
    url_lists.append(v_url)
    # 视频存在多集的情况
    page_patn = re.compile('index__part__src-videoPage-multiP-part')
    html_page = re.findall(page_patn, html_str)
    # 其它集加入list
    if html_page:
        pagesize = len(html_page)
        print(f'共有{pagesize}个分集')
        for i in range(1,pagesize+1):
            html_str2 = parse_url(url+'/?p='+str(i))
            try:
                v_url = re.findall(url_patn, html_str2)[0]
            except:
                return
            v_url = 'http:'+v_url
            url_lists.append(v_url)
    else:
        print('没有分集')

    return url_lists

def download_begin(url_lists, title, author):
    '''
    函数描述：开始下载，构造下载分类的文件夹，调用下载的模块
    入口参数：url列表，视频标题和视频作者
    出口参数：无
    '''
    title = sub(title)
    proxies = get_proxies()
    for index,v_url in enumerate(url_lists):
        path = './video/'+ author +'/'
        # 创建文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        download_video(v_url,path, title+str(index+1), proxies)

def download_video(v_url,path,title,proxies):
    '''
    函数描述：下载模块,简单进度条显示
    入口参数：视频地址、保存路径、标题、代理ip
    出口参数：无
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    video = requests.get(url=v_url, headers=headers,verify=False, proxies=proxies,stream=True)
    if video.status_code == 200:
        video_size = int(video.headers['content-length'])
        print(f'视频大小为{round(video_size/(1024*1024),2)}MB')
        with ProgressBar(max_value=video_size) as bar:
            jd = 0
            with open(path+title+'.mp4','wb') as f:
                for chunk in video.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(jd)
                        jd = jd + 1024
        print('下载成功')
    else:
        print('下载失败')

def main():
    # up主的id
    up_mid = '10957838'
    video_List = get_response(up_mid)
    v_num = len(video_List)
    print(f'共有{v_num}个投稿')
    index = 0
    for video in video_List:
        video_aid = video['aid']
        video_title = video['title']
        video_author = video['author']
        index += 1
        print(f'开始下载，现在正在下载第{index}/{v_num}个视频')
        url_lists = parse_download_url(video_aid)
        download_begin(url_lists, video_title, video_author)
        # print(url_lists)
        sleep(1)

if __name__ == '__main__':
    main()
    # video_aid = 57696128
    # url_lists = parse_download_url(video_aid)
    # print(len(url_lists))
