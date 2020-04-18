#!/bin/env python
# -*- coding:utf-8 -*-
from urllib import parse
import requests
from bs4 import BeautifulSoup
#http://s.dydytt.net/plus/search.php?keyword=%BF%C6%BB%C3&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=10&typeid=0&TotalResult=279&PageNo=4
class get_urldic:
    def __init__(self):
        self.first_url = 'http://s.dydytt.net/plus/search.php?'
        self.second_url = '&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=10&typeid=0&TotalResult=279&PageNo='
        self.info_url = 'http://s.dydytt.net'
    #获取搜索关键字
    def get_url(self):
        urlList = []
        # first_url = 'http://s.dydytt.net/plus/search.php?'
        # second_url = '&searchtype=titlekeyword&channeltype=0&orderby=&kwtype=0&pagesize=10&typeid=0&TotalResult=279&PageNo='
        try:
            search = input("Please input search name:")
            dic = {'keyword':search}
            keyword_dic = parse.urlencode(dic,encoding='gb2312')
            page = int(input("Please input page:"))
        except Exception as e:
            print('Input error:',e)
            exit()
        for num in range(1,page+1):
            url = self.first_url + str(keyword_dic) + self.second_url + str(num)
            urlList.append(url)
        print("Please wait....")
        print(urlList)
        return urlList,search

    #获取网页文件
    def get_html(self,urlList):
        response_list = []
        for r_num in urlList:
            request = requests.get(r_num)
            response = request.content.decode('gbk','ignore').encode('utf-8')
            response_list.append(response)
        return response_list

    #获取blog_name和blog_url
    def get_soup(self,html_doc):
        result = {}
        for g_num in html_doc:
            soup = BeautifulSoup(g_num,'html.parser')
            context = soup.find_all('td', width="55%")
            for i in context:
                title=i.get_text()
                result[title.strip()]=self.info_url + i.b.a['href']
        return result

    def get_info(self,info_dic):
        info_tmp = []
        for k,v in info_dic.items():
            print(v)
            response = requests.get(v)
            new_response = response.content.decode('gbk').encode('utf-8')
            soup = BeautifulSoup(new_response, 'html.parser')
            info_dic = soup.find_all('div', class_="co_content8")
            info_list1= []
            for context in info_dic:
                result = list(context.get_text().split())
                for i in range(0, len(result)):
                    if '发布' in result[i]:
                        public = result[i]
                        info_list1.append(public)
                    elif "豆瓣" in result[i]:
                        douban = result[i] + result[i+1]
                        info_list1.append(douban)
                    elif "【下载地址】" in result[i]:
                        download = result[i] + result[i+1]
                        info_list1.append(download)
                    else:
                        pass
            info_tmp.append(info_list1)
        return info_tmp

if __name__ == '__main__':
    blog = get_urldic()
    urllist, search = blog.get_url()
    html_doc = blog.get_html(urllist)
    result = blog.get_soup(html_doc)
    for k,v in result.items():
        print('search blog_name is:%s,blog_url is:%s' % (k,v))
    info_list = blog.get_info(result)
    for list in info_list:
        print(list)