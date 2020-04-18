#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

import requests
from bs4 import BeautifulSoup
import random

class GetProxyIP:

    def __init__(self,page=10):
        self._page = page
        self.url_head = 'http://www.xicidaili.com/wt/'

    def get_ip(self):
        """
        get resouce proxy ip pool
        :return: res_pool list
        """
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        res_pool = []
        for pagenum in range(1,self._page):
            url = self.url_head + str(pagenum)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            soup_tr = soup.find_all('tr')
            for item in soup_tr:
                try:
                    soup_td = item.find_all('td')
                    res_pool.append(soup_td[5].text.lower() + '://' + soup_td[1].text + ':' + soup_td[2].text)
                except IndexError:
                    pass
        return res_pool

    def right_proxies(self,res_pool):
        """
        check available ip
        :param res_pool:
        :return:right_pool list
        """
        right_pool = []
        for ip in res_pool:
            if 'https' in ip:
                proxies = {'http': ip}
            else:
                proxies = {"http": ip}
            check_urllist = ['http://www.baidu.com', 'http://www.taobao.com', 'https://cloud.tencent.com/']
            try:
                response = requests.get(random.choice(check_urllist), proxies=proxies, timeout = 1)
                if response.status_code:
                    right_pool.append(proxies)
                    print('add ip %s' % proxies)
            except Exception as e:
                continue
        return right_pool

if __name__ == '__main__':
    proxyhelper = GetProxyIP(2)
    res_pool = proxyhelper.get_ip()
    proxy_ip =proxyhelper.right_proxies(res_pool)
    print(proxy_ip)
