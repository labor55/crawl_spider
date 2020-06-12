import requests
from retrying import retry

'''
专门请求url地址的方法
'''
#headers = {"User-Agent" : "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"}
headers = {
    "User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }


#让被装饰的的函数反复执行3次，三次全部报错，则函数报错，若有一次正确，程序继续往下运行
@retry(stop_max_attempt_number=3)
def _parse_url(url):
    response = requests.get(url,headers = headers,timeout=3, verify=False)
    return response.text


def parse_url(url):
    try:
        html_str = _parse_url(url)
    except:
        html_str= None
    return html_str

if __name__=='__main__':
    url="http://www.baidu.com"
    print(parse_url(url)[:100])
