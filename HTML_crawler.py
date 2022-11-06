# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/06/18
#           Version:
#             Description: 爬取Html框架（用类重写）
# ==========================================
# 导入库
from urllib import request, parse
from bs4 import BeautifulSoup
import traceback


class Get:
    '''
    爬取目标HTML页面并返回页面原始Body
    '''

    def __init__(self, url):
        self.url = url

    def GetData(self):
        '''
        用于爬取目的网址HTML网页内容 的函数
        参数：
        url 需要爬取内容的网址

        该函数是从网页中爬取数据，并保存在一个列表中
        需要寻找对应数据请看示例：

        用 Beautiful Soup 方法解析网页结构，用find（）找到对应的标签。
        data = body.find('div', {'class': 'info clearfix'})  # 找到对应的标签
        '''
        req = request.Request(url=self.url)  # 用requests抓取网页信息
        res = request.urlopen(req)
        res_text = res.read().decode('utf-8')
        # 用BeautifulSoup库解析网页
        soup = BeautifulSoup(res_text, 'html.parser')
        body = soup.body
        return body
