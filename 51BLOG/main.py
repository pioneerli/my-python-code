#!/bin/env python
# -*- coding:utf-8 -*-


import geturl3
import getexcel3

#获取url字典
def get_dic():
    blog = geturl3.get_urldic()
    urllist, search = blog.get_url()
    html_doc = blog.get_html(urllist)
    result = blog.get_soup(html_doc)
    return result,search

#写入excle
def write_excle(urldic,search):
    excle = getexcel3.create_excle()
    workbook, worksheet = excle.create_workbook(search)
    excle.col_row(worksheet)
    merge_format, name_format, normal_format = excle.shell_format(workbook)
    excle.write_title(worksheet,search,merge_format)
    excle.write_tag(worksheet,name_format)
    excle.write_context(worksheet,urldic,normal_format)
    excle.workbook_close(workbook)

def main():
    url_dic ,search_name = get_dic()
    write_excle(url_dic,search_name)

if __name__ == '__main__':
    main()