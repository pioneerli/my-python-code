#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

import memcache
import random
import configparser
import spider

class MemcacheOper:

    def __init__(self):
        """
        initialization redis infomation
        :param
        """
        config = configparser.ConfigParser()
        config.read('db.conf')
        self.host = config['memcache']['HOST']
        self.port = config['memcache']['PORT']
        self.mcoper = memcache.Client([self.host+':'+self.port], debug = True)

    def memcache_save(self,result_list):
        """
        save data
        :return:None
        """
        for num,cont in enumerate(result_list):
            self.mcoper.set(str(num),cont)

    def memcache_gain(self):
        """
        gain data
        :return: proxies
        """
        num = random.randint(0,10)
        ip = self.mcoper.get(str(num))
        return ip

if __name__ == '__main__':
    proxyhelper = spider.GetProxyIP(2)
    res_pool = proxyhelper.get_ip()
    proxy_ip = proxyhelper.right_proxies(res_pool)
    dbhelper = MemcacheOper()
    dbhelper.memcache_save(proxy_ip)
    ip = dbhelper.memcache_gain()
    print(ip)