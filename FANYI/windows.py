#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

import tkinter as tk
from fanyi import search

class application:
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title("翻译小工具")
        self.windows.geometry("280x350+700+300")


        #提交按钮
        self.submit_btn = tk.Button(self.windows, text="查询",command=self.submit)
        self.submit_btn.place(x=220, y=10, width=50, height=25)

        # 定义输入框
        self.entry = tk.Entry(self.windows)
        self.entry.place(x=10, y=10, width=200, height=40)

        #输出内容
        self.result_text = tk.Text(self.windows, background="#ccc")
        self.result_text.place(x=10, y=90, width=260, height=245)

        # 翻译结果标题
        self.title_label = tk.Label(self.windows, text="翻译结果：")
        self.title_label.place(x=10, y=65)

        self.search_result = search()

    def submit(self):
        #1.获取用户输入
        context = self.entry.get()

        #2.利用有道翻译
        result = self.search_result.main(context)
        #3.输出
        self.result_text.delete(1.0,tk.END)
        self.result_text.insert(tk.END,result)


    def run(self):

        self.windows.mainloop()


if __name__ == '__main__':
    winapp = application()
    winapp.run()


