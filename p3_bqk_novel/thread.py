import threading
from queue import Queue
import requests
from lxml import etree
from time import sleep

class Crawl_thread(threading.Thread):
    def __init__(self, thread_id, queue):
        self.threading.Thread.__init__()
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            else:
                page = self.queue.get()
                print(f'当前正在工作的线程是{self.thread_id},正在采集')
                url = '' # page页面的url
                headers = {}
                try:
                    content = requests.get(url=url, headers=headers)
                    data_queue.put(content.text) # .............

                except Exception as e:
                    print(f'采集线程错误:{e}')

class Parse_Thread(threading.Thread):
    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        print(f'启动了线程:{self.thread_id}')
        while not flag:
            try:
                item = self.queue.get(False)
                if not item:
                    pass
                self.parse_data(item)
                # queue.task_done()执行完一次后，发送执行成功的信号，以便下个执行开始或者介绍执行
                self.queue.task_done() # 用来判断
            except Exception as e:
                raise
        print(f'退出了线程:{self.thread_id}')

    def parse_data(self, item):
        html = etree.HTML(item)
        result = html.xpath('')



data_queue = Queue()
flag = False

def main():
    pageQueue = Queue(50)
    for page in range(1,11):
        pageQueue.put(page)

    Crawl_threads = []
    Crawl_name_list = ['crawl_1','crawl_2','crawl_3']
    for thread_id in Crawl_name_list:
        thread = Crawl_thread(thread_id, pageQueue)
        thread.start()
        Crawl_threads.append(thread)

    Parse_Threads =[]
    Parse_name_list = ['parse_1','parse_2','parse_3']
    for thread_id in Parse_name_list:
        thread = Parse_Thread(thread_id, data_queue)
        thread.start()
        Parse_Threads.append(thread)

    while not pageQueue.empty():
        pass
    for t in Crawl_threads:
        t.join()
    while not data_queue.empty():
        pass
    global flag
    flag = True
    for t in Parse_Threads:
        t.join()
    print('退出主线程')


main()
