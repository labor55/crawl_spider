import requests
import re
from progressbar import ProgressBar
from contextlib import closing

'''
代码功能：下载音悦台MV，到本地文件夹
入口参数：音悦台MV的URL
出口参数：无
代码实现：音悦台mv的下载地址在为---http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId= + {mv_num}---,
        用get方法请求此url, 用正则匹配，可以得到MV的真正下载地址，
代码特色：使用ProgressBar 实现了下载进度条的实时跟进
'''


class YinYueTai_MV():
    def __init__(self, mv_url):
        self.mv_url = mv_url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}

    def main(self):
        mv_num = self.mv_url.split('/')[-1].strip()
        # 此链接请求结果为MV的信息，然后分析此结果，获取mv链接等
        info_url = f'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId={mv_num}'
        info_res = requests.get(url=info_url, headers=self.headers)
        # 获取到视频链接列表
        p = re.compile(r'http://\w.*?\.yinyuetai.com/uploads/videos/common/.*?(?=&br)')
        mv_urls = re.findall(p, info_res.text)

        # 选择清晰度
        num = len(mv_urls)
        print(f'可选择的清晰度有{num}种,')
        choice = input(f'请选择清晰度(0-{num-1})（数字越高越清晰）>>: ')

        # 清晰度选择列表
        choice_list = [str(i) for i in range(num)]
        # 检查输入
        if choice in choice_list:
            mv_url = mv_urls[int(choice)]
            print(f'下载的视频地址为{mv_url}')
            with closing(requests.get(url=mv_url, headers=self.headers, stream=True)) as mv:
                if mv.status_code == 200:
                    # 获取文件大小
                    mv_size = int(mv.headers['content-length'])
                    print(f'请求成功,文件大小为{mv_size/(1024*1024)}MB')
                    print('正在下载,请稍等')
                    with ProgressBar(max_value=mv_size) as bar:
                        jd = 0
                        # 下载视频
                        with open(f'{mv_num}_{choice}.mp4', 'wb') as f:
                            # 分块传输，每一块大小为1024
                            for chunk in mv.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                                    bar.update(jd) # 进度条
                                    jd = jd + 1024
                    print('下载完成。。。')
                else:
                    print('connect error')
        else:
            print('选择错误，请重新选择')
            print('*'*10)
            print('\n'*2)
            return self.main()

if __name__ == '__main__':
    url = input('请输入mv的url地址 -- mv_url>> ')
    yin = YinYueTai_MV(url)
    yin.main()
