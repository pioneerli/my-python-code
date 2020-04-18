#!/bin/env python
# -*- coding:utf-8 -*-
# @Author  : kaliarch

import xlsxwriter

class create_excle:
    def __init__(self):
        self.tag_list = ["movie_name", "movie_url"]
        self.info = "information"

    def create_workbook(self,search=" "):
        excle_name = search + '.xlsx'
        #定义excle名称
        workbook = xlsxwriter.Workbook(excle_name)
        worksheet_M = workbook.add_worksheet(search)
        worksheet_info = workbook.add_worksheet(self.info)
        print('create %s....' % excle_name)
        return workbook,worksheet_M,worksheet_info

    def col_row(self,worksheet):
        worksheet.set_column('A:A', 12)
        worksheet.set_row(0, 17)
        worksheet.set_column('A:A',58)
        worksheet.set_column('B:B', 58)

    def shell_format(self,workbook):
        #表头格式
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#FAEBD7'
        })
        #标题格式
        name_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#E0FFFF'
        })
        #正文格式
        normal_format = workbook.add_format({
            'align': 'center',
        })
        return merge_format,name_format,normal_format

    #写入title和列名
    def write_title(self,worksheet,search,merge_format):
        title = search + "搜索结果"
        worksheet.merge_range('A1:B1', title, merge_format)
        print('write title success')

    def write_tag(self,worksheet,name_format):
        tag_row = 1
        tag_col = 0
        for num in self.tag_list:
            worksheet.write(tag_row,tag_col,num,name_format)
            tag_col += 1
        print('write tag success')

    #写入内容
    def write_context(self,worksheet,con_dic,normal_format):
        row = 2
        for k,v in con_dic.items():
            if row > len(con_dic):
                break
            col = 0
            worksheet.write(row,col,k,normal_format)
            col+=1
            worksheet.write(row,col,v,normal_format)
            row+=1
        print('write context success')

    def write_info(self,worksheet_info,info_list,normal_format):
        row = 1
        for infomsg in info_list:
            for num in range(0,len(infomsg)):
                worksheet_info.write(row,num,infomsg[num],normal_format)
                num += 1
            row += 1

        print("wirte info success")


    #关闭excel
    def workbook_close(self,workbook):
        workbook.close()


if __name__ == '__main__':
    print('This is create excel mode')
