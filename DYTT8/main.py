#!/bin/env python
# -*- coding:utf-8 -*-


import geturldytt
import getexceldytt

#获取url字典
def get_dic():
    blog = geturldytt.get_urldic()
    urllist, search = blog.get_url()
    html_doc = blog.get_html(urllist)
    result = blog.get_soup(html_doc)
    info_list= blog.get_info(result)
    return result,search,info_list

#写入excle
def write_excle(urldic,search,info_list):
    excle = getexceldytt.create_excle()
    workbook, worksheet, worksheet_info = excle.create_workbook(search)
    excle.col_row(worksheet)
    merge_format, name_format, normal_format = excle.shell_format(workbook)
    excle.write_title(worksheet,search,merge_format)
    excle.write_tag(worksheet,name_format)
    excle.write_context(worksheet,urldic,normal_format)
    excle.write_info(worksheet_info,info_list,normal_format)
    excle.workbook_close(workbook)

def main():
    url_dic ,search_name, info_list = get_dic()
    write_excle(url_dic,search_name,info_list)

if __name__ == '__main__':
    main()