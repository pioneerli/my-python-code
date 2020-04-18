#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

import requests
from bs4 import BeautifulSoup
import urllib
import os
import threading

class DutuSpider():
    # 定义全局页面url列表
    page_url_list = []
    # 定义具体各表情图片url列表
    img_url_list = []
    # 定义rlock进程锁
    rlock = threading.RLock()

    def __init__(self,page_number=10,img_dir='imgdir',thread_number=5):
        """
        :param page_number: 抓去多少个页面，默认10
        :param img_dir: 定义图片目录
        :param thread_number:默认5个线程
        """
        self.spider_url = 'https://www.doutula.com/photo/list/?page='
        self.page_number = int(page_number)
        self.img_dir = img_dir
        self.thread_num = thread_number


    def get_url(self):
        """
        创建image目录和生产pageurl列表
        :return:
        """
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        for page in range(1,self.page_number+1):
            DutuSpider.page_url_list.append(self.spider_url + str(page))

    def __set_header(self):
        """
        定义header
        :return:
        """
        header = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        }
        return header

    def __add_urllist(self):
        """
        定义从page_url_list 爬取具体的image的url
        :return:
        """
        while True:
            DutuSpider.rlock.acquire()
            if len(DutuSpider.page_url_list) == 0:
                DutuSpider.rlock.release()
                break
            else:
                page_url = DutuSpider.page_url_list.pop()
                DutuSpider.rlock.release()
                response = requests.get(page_url, headers=self.__set_header())
                soup = BeautifulSoup(response.content,'lxml')
                sou_list = soup.find_all('img',attrs={'class':'img-responsive lazy image_dta'})
                # 将获取到的具体表情图标的url保存添加进img_url_list 列表
                for url_content in sou_list:
                    DutuSpider.rlock.acquire()
                    DutuSpider.img_url_list.append(url_content['data-original'])
                    DutuSpider.rlock.release()



    def __download_img(self):
        """
        从image_url_list中来下载image到本地
        :return:
        """
        while True:
            DutuSpider.rlock.acquire()
            if len(DutuSpider.img_url_list) == 0:
                DutuSpider.rlock.release()
                continue
            else:
                img_url = DutuSpider.img_url_list.pop()
                DutuSpider.rlock.release()
                try:
                    # 图片名称
                    img_name = img_url.split('/')[-1]
                    # 下载图片
                    urllib.urlretrieve(img_url,os.path.join(self.img_dir,img_name))
                    print('donload img %s' % img_name)
                except Exception as e:
                    pass


    def run(self):
        # 启动thread_num个进程来爬去具体的img url 链接
        for th in range(self.thread_num):
            add_pic_t = threading.Thread(target=self.__add_urllist)
            add_pic_t.start()

        # 启动thread_num个来下载图片
        for img_th in range(self.thread_num):
            download_t = threading.Thread(target=self.__download_img)
            download_t.start()



if __name__ == '__main__':
    spider = DutuSpider(page_number=10,img_dir='imgdir',thread_number=7)
    spider.get_url()
    spider.run()


