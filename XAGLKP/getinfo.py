#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch
import re
import requests
from bs4 import BeautifulSoup

class Getinformation:
    def __init__(self):
        """init url"""
        self.init_url = 'http://www.xaglkp.com/ClassSearch/IndexPost'

    def getsoup(self):
        """:return soup"""
        response = requests.post(self.init_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def getStartAddress(self,soup):
        """get start address dict"""
        staraddress = soup.find_all('option', text=re.compile("\w+客运站"))
        num_list = [1000]
        add_list = ["全部"]
        for num in staraddress:
            num_list.append(num['value'])
            add_list.append(num.text)
        startaddrdict = dict(zip(add_list, num_list))
        return startaddrdict

    def getStartDate(self,soup):
        """get time"""
        date = soup.find_all('option', text=re.compile("2018.*?"))
        date_list = []
        for num in date:
            date_list.append(num.text)
        return date_list

    def getStartTime(self,soup):
        """
        get start time
        :return start time list
        """
        times = soup.find_all('option', text=re.compile("\w.*?后"))
        time_list = ['05:00后']
        for num in times:
            time_list.append(num.text)
        return time_list



if __name__ == '__main__':
    test = Getinformation()
    soup = test.getsoup()
    add = test.getStartAddress(soup)
    print(add)

