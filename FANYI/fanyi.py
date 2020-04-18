#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch
import requests
import urllib.parse
import time
import random
import hashlib
import json

class search(object):
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'


    def getData(self,search_name):
        # salt =i = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)
        salt = ((time.time() * 1000) + random.randint(1,10))
        # sign = n.md5("fanyideskweb" + t + i + "ebSeFb%=XZ%T[KZ)c(sy!")
        sign_text = "fanyideskweb" + search_name + str(salt) + "ebSeFb%=XZ%T[KZ)c(sy!"
        sign = hashlib.md5((sign_text.encode('utf-8'))).hexdigest()
        paydata = {
            'i': search_name,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': 'false'
        }
        return paydata

    def getHeader(self):
        header = {
            'Host': 'fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-846616837@1.80.219.201; OUTFOX_SEARCH_USER_ID_NCOO=129549097.60835753; UM_distinctid=15ff309f18ddc-094cb5494ad815-5d4e211f-1fa400-15ff309f18e449; _ga=GA1.2.184261795.1517119351; __guid=204659719.2556877880764680700.1518435624954.942; JSESSIONID=aaa3A5BLhtTrh4TPX_mgw; monitor_count=2; ___rl__test__cookies=1518488731567'
        }
        return header

    def getRequest(self,paydata,header):
        _data = urllib.parse.urlencode(paydata).encode('utf-8')
        _header = header
        response = requests.post(self.url,data=_data,headers=_header)
        return response.text

    def getResult(self,response):
        result_text = json.loads(response)
        #src = result_text['translateResult'][0][0]['src']
        tgt = result_text['translateResult'][0][0]['tgt']
        return tgt

    def main(self,search_name):
        app = search()
        paydata = app.getData(search_name)
        header = app.getHeader()
        response = app.getRequest(paydata, header)
        tgt = app.getResult(response)
        return tgt
