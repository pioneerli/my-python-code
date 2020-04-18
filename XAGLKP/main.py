#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

import getinfo
import requests
from bs4 import BeautifulSoup

oper = getinfo.Getinformation()
soup = oper.getsoup()

startdic = oper.getStartAddress(soup)
startdate = oper.getStartDate(soup)
starttime = oper.getStartTime(soup)
init_url = 'http://www.xaglkp.com/ClassSearch/IndexPost'

def getSadd():
    """get input start address"""
    print("起始站如下:")
    print("*" * 20)
    for v in startdic.keys():
        print(v)
    print("*" * 20)
    trynum = 0
    start = str(input("请输入出发地点:"))
    while trynum < 5:
        for v in startdic.keys():
            if start == v:
                return startdic[start]
        else:
            print("输入错误，还有%d次重试机会" % (5-trynum))
            start = str(input("请从新输入出发地点:"))
        trynum += 1

def getDes():
    """get input destination address"""
    try:
        destadd = str(input("请输入目的地:"))
        result = 1
    except Exception as e:
        print("输入错误：",e)
    if result:
        return destadd

def getDate():
    """get input start date"""
    print("出发日期如下:")
    print("*" * 20)
    for date in startdate:
        print(date)
    print("*" * 20)
    trynum = 0
    date1 = str(input("请输入出发时间:"))
    while trynum < 5:
        for i in startdate:
            if date1 == i:
                return date1
        else:
            print("输入错误，还有%d次重试机会" % (5-trynum))
            date1 = str(input("请从新输入出发时间:"))
        trynum += 1

def getTime():
    """get input start time"""
    print("出车时间如下**(05:00表示所有)**:")
    print("*" * 20)
    for time in starttime:
        print(time)
    print("*"*20)
    trynum = 0
    time1 = str(input("请输入发车时间(05:00表示所有):"))
    while trynum < 5:
        for i in starttime:
            if time1 == i:
                return time1.split('后')[0]
        else:
            print("输入错误，还有%d次重试机会" % (5-trynum))
            time1 = str(input("请从新输入发车时间(05:00表示所有):"))
        trynum += 1

def getPayData():
    """get requests paydata"""
    sadd = getSadd()
    desadd = getDes()
    sdate = getDate()
    stime = getTime()
    paydata = {
        'selected':sadd,
        'Arrive':desadd,
        'selected1':sdate,
        'selected2':stime,
        'page':'',
        'ArriveHidden':sadd,
    }
    return paydata

def getHeader():
    """get request headers"""
    header = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'www.xaglkp.com',
        'Referer':'http://www.xaglkp.com/ClassSearch/IndexPost',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    return header



def get_request():
    """requests"""
    header = getHeader()
    paydata = getPayData()
    select_result = requests.post(init_url,headers=header,data=paydata)
    result_soup = BeautifulSoup(select_result.text, 'html.parser')
    result = result_soup.find_all('table')
    return result


def format_list():
    result_L = get_request()
    L1 = []
    for context in result_L:
        L1.append(context.text)
    tmp = '\n'.join(L1)
    str = tmp.replace("\n"," ")
    L2 = []
    for i2 in str.split():
        L2.append(i2)
    return L2

def title_context():
    """get title list,get context list"""
    result_L = format_list()
    print("共搜索出%d趟车!详细信息如下:" % int(len(result_L) / 9))

    title_L = []
    title = 0
    for i in result_L[title:title + 9]:
        title_L.append(i)
    print(title_L)

    totle_L = []
    num = 9
    for i in range(0, len(result_L) // 9):

        context_L = []
        for n in result_L[num:num + 8]:
            context_L.append(n)
        print(context_L)

        totle_L.append(context_L)
        num += 8
        if i > int(len(result_L) / 9):
            exit()

if __name__ == '__main__':
    title_context()