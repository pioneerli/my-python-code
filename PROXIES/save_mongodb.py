#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch



import configparser
import spider
from pymongo import MongoClient

class MongodbOper:

    def __init__(self):
        """
        initialization redis infomation
        :param
        """
        config = configparser.ConfigParser()
        config.read('db.conf')
        self.host = config['mongodb']['HOST']
        self.port = config['mongodb']['PORT']
        self.db = config['mongodb']['DB']
        self.user = config['mongodb']['USER']
        self.pwd = config['mongodb']['PASSWD']
        self.client = MongoClient(self.host, int(self.port))
        self.db_auth = self.client.admin
        self.db_auth.authenticate(self.user,self.pwd)
        self.DB = self.client[self.db]
        self.collection = self.DB.myset

    def mongodb_save(self,result_list):
        """
        save data
        :return:None
        """

        for values in result_list:
            self.collection.insert(values)

    def mongodb_gain(self):
        """
        gain data
        :return: proxies
        """
        ip = self.collection.find_one()
        return ip

if __name__ == '__main__':
    proxyhelper = spider.GetProxyIP(2)
    res_pool = proxyhelper.get_ip()
    proxy_ip = proxyhelper.right_proxies(res_pool)
    dbhelper = MongodbOper()
    dbhelper.mongodb_save(proxy_ip)
    ip = dbhelper.mongodb_gain()
    print(ip)