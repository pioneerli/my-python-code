#!/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class get_urldic:
    #获取搜索关键字
    def get_url(self):
        urlList = []
        first_url = 'http://blog.51cto.com/search/result?q='
        after_url = '&type=&page='
        try:
            search = input("Please input search name:")
            page = int(input("Please input page:"))
        except Exception as e:
            print('Input error:',e)
            exit()
        for num in range(1,page+1):
            url = first_url + search + after_url + str(num)
            urlList.append(url)
        print("Please wait....")
        return urlList,search

    #获取网页文件
    def get_html(self,urlList):
        response_list = []
        for r_num in urlList:
            request = requests.get(r_num)
            response = request.content
            response_list.append(response)
        return response_list

    #获取blog_name和blog_url
    def get_soup(self,html_doc):
        result = {}
        for g_num in html_doc:
            soup = BeautifulSoup(g_num,'html.parser')
            context = soup.find_all('a',class_='m-1-4 fl')
            for i in context:
                title=i.get_text()
                result[title.strip()]=i['href']
        return result



if __name__ == '__main__':
    blog = get_urldic()
    urllist, search = blog.get_url()
    html_doc = blog.get_html(urllist)
    result = blog.get_soup(html_doc)
    for k,v in result.items():
        print('search blog_name is:%s,blog_url is:%s' % (k,v))