#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


class BlogSave():
    # 定义headers字段
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
    }

    def __init__(self,blog_name,page_number,login_user_name,login_passwd):
        self.login_url = 'http://home.51cto.com/index'
        # 博客用户名
        self.blog_name = blog_name
        # 需要保存的博客多少页
        self.page_number = page_number
        # 登陆的用户
        self.login_user_name = login_user_name
        # 登陆的密码
        self.login_passwd = login_passwd
        # 本地的chreomedriver驱动
        self.chromedirve = 'D:\chromedriver.exe'
        # blog 导入url
        self.blog_save_url = 'http://blog.51cto.com/blogger/publish/'


    def get_urldict(self):
        """
        爬去用户文章的url
        :param pagenumber:
        :return: urllist
        """
        content_dict = {}
        scrapy_urllist = ["http://blog.51cto.com/" + str(self.blog_name) + "/p" + str(page) for page in
                          range(1, int(self.page_number) + 1)]
        for scrapy_url in scrapy_urllist:
            response = requests.get(scrapy_url, headers=BlogSave.headers)
            soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
            title_list = soup.find_all('a', class_='tit')

            for content in title_list:
                # 获取url
                url = content['href']
                title_soup = BeautifulSoup(requests.get(url, headers=BlogSave.headers).content, 'lxml', from_encoding='utf-8')
                title = title_soup.find_all('h1', class_='artical-title')
                # 获取标题
                # print(title[0].get_text())
                content_dict[title[0].get_text()] = url
                print(title[0].get_text(),url)

        return content_dict


    def save_blog(self,url_list):
        """
        通过模拟登陆保存博客文件
        :return:
        """
        browser = webdriver.Chrome(self.chromedirve)
        # 打开url
        browser.get(self.login_url)
        time.sleep(2)
        # 登陆
        browser.find_element_by_id('loginform-username').send_keys(self.login_user_name)
        browser.find_element_by_id('loginform-password').send_keys(self.login_passwd)
        browser.find_element_by_name('login-button').click()
        time.sleep(1)
        for url in url_list:
            browser.get(url)
            time.sleep(1)
            try:
                browser.find_element_by_xpath('//*[@id="blogEditor-box"]/div[1]/a[14]').click()
                time.sleep(2)
            except Exception as e:
                with open('fail.log','a') as f:
                    f.write(url + str(e))

    def run(self):
        # 获取标题和url字典
        content_dict = self.get_urldict()
        # 获取url列表
        id_list = []
        for value in content_dict.values():
            id_list.append(str(value).split('/')[-1])
        result_list = [ self.blog_save_url + str(id) for id in id_list ]
        print("result_list:",result_list)
        self.save_blog(result_list)

if __name__ == '__main__':
    # blogOper = BlogSave('kaliarch',1)
    # dict = blogOper.get_urldict()
    # value_list = [ value for value in dict.values()]
    # print(value_list)
    blogOper = BlogSave(blog_name='kaliarch',page_number=5,login_user_name='xxxxxxxxxxxxx@163.com',login_passwd='qxxxxxxxxx')
    blogOper.run()
