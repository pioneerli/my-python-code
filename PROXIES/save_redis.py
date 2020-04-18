#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

import redis
import random
import configparser
import spider

class RedisOper:

    def __init__(self):
        """
        initialization redis infomation
        :param
        """
        config = configparser.ConfigParser()
        config.read('db.conf')
        self.host = config['redis']['HOST']
        self.port = config['redis']['PORT']
        self.passwd = config['redis']['PASSWD']
        self.pool = redis.ConnectionPool(host=self.host,port=self.port,password=self.passwd)
        self.redis_helper = redis.Redis(connection_pool=self.pool)
        self.pipe = self.redis_helper.pipeline(transaction=True)

    def redis_save(self,result_list):
        """
        save data
        :return:None
        """
        for num,cont in enumerate(result_list):
            self.redis_helper.set(num,cont)
        self.pipe.execute()

    def redis_gain(self):
        """
        gain data
        :return: proxies
        """
        num = random.randint(0,10)
        ip = self.redis_helper.get(num)
        self.pipe.execute()
        return ip

if __name__ == '__main__':
    # proxyhelper = spider.GetProxyIP(2)
    # res_pool = proxyhelper.get_ip()
    # proxy_ip = proxyhelper.right_proxies(res_pool)
    dbhelper = RedisOper()
    # dbhelper.redis_save(proxy_ip)
    ip = dbhelper.redis_gain()
    print(ip)