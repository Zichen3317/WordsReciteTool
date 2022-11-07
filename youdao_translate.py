# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/11/05
#           Version:
#             Description: 有道翻译网页爬虫数据处理库
# ==========================================
import HTML_crawler


class translate:
    def __init__(self, word) -> None:
        self.word = word
        base_url = 'https://dict.youdao.com/search?q=%s&keyfrom=new-fanyi.smartResult' % word
        self.Data = HTML_crawler.Get(url=base_url).GetData()

    # 翻译

    def Get_Zh_trans(self):
        try:
            Lst_temp = []
            Zh_trans_lst = self.Data.find(
                'div', {'class': 'trans-container'}).find('ul').find_all('li')
            for i in Zh_trans_lst:
                Lst_temp.append(i.string)
            return '|'.join(Lst_temp)  # 中文翻译可能有多个词性
        except AttributeError:
            print('ERROR:无法查到%s的中文翻译！' % self.word)

    # 音标

    def Get_Pronounce(self):
        try:
            Pronounce_Total = self.Data.find('div', {'class': 'baav'}).find_all(
                'span', {'class': 'pronounce'})
            Pronounce_list = []
            for i in Pronounce_Total:
                Pronounce_list.append(
                    i.get_text().replace(' ', '').replace('\n', ''))
            return Pronounce_list
        except AttributeError:
            print('ERROR:无法查到%s的读音！' % self.word)
            return None

    # 例句

    def Get_Example_Sentences(self):

        Example_Sentences_list = []  # 用于存放例句和对应解释的列表
        try:
            Example_Sentences_temp = self.Data.find(
                'ul', {'class': 'ol'}).find_all('li')  # 列表
            for i in Example_Sentences_temp:
                try:  # 有的英文解释没例句，获取会报错
                    # 同时获取英文解释和例句，排序为[解释,例句]
                    Example_Sentences_list.append(
                        [i.find('span', {'class': 'def'}).string, i.find_all('p')[0].find('em').string])
                except:
                    pass
            return Example_Sentences_list
        except AttributeError:
            print('ERROR:无法查到%s的英文解释' % self.word)
            return None


print(translate('escalate').Get_Pronounce())
