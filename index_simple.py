# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/11/05
#           Version:
#             Description:调用百度翻译api实现单词录入，用csv库存储单词并调用
# ==========================================
import baidu_translate
import CSVTool
import traceback
import os
import random

# 简易版本
Ver = '1.1.0_simple_Alpha'


def main():
    IN_Content_Dict_list = []  # 存放单词的地方
    IN_Content_list = []
    header_list = ["en", "zh"]  # 表头
    print('WordsReciteTool %s Service Start' % Ver)
    CMD = input('R/W ?\nTip:输入R进入背诵模式,W进入录入模式\n>>>')
    if CMD == 'W':
        # 录入模式
        f_name = input('\n请输入单词本名\n>>>>>>')
        # 初始化
        f_path = '.\\%s.csv' % f_name
        CSVtool = CSVTool.Tool(f_path)
        if os.path.exists(f_path) == True:
            model = '追加'
        else:
            model = '新创建'
        print(
            '\n==========\n已完成初始化\n模式:%s\n==========\n请输入需要录入的单词(输入 /finish 来完成录入)' % model)
        while True:
            Word_en = input('>>>')
            if Word_en != '/finish':
                try:  # 有可能出现录入错误,若此单词录入错误就报错，然后继续
                    Word_zh = baidu_translate.translate(Word_en)
                    # 注意如果文件已经存在，则调用不同的方法，要求的输入数据格式不同
                    if os.path.exists(f_path) == True:
                        IN_Content_list.append([Word_en, Word_zh])
                    else:
                        IN_Content_Dict_list.append(
                            {'en': Word_en, 'zh': Word_zh})
                    print('{} - {} - ✓'.format(Word_en, Word_zh))
                except:
                    traceback.print_exc()
                    pass
            else:
                break
        # 注意如果文件已经存在就不再重复写入
        if os.path.exists(f_path) == True:  # 存在
            CSVtool.ADD(IN_Content_list)
            print('[追加]单词本名:{} - 写入 - ✓'.format(f_name+'.csv'))
        else:  # 不存在
            CSVtool.WRITE(header_list, IN_Content_Dict_list)
            print(
                '[新创建]单词本名:{} - 写入 - ✓\nTip:单词本已创建在本程序的同级文件夹内，除删除之外请勿随意移动此文件'.format(f_name+'.csv'))
        os.system('pause')
    elif CMD == 'R':
        # 背诵模式
        f_name = input('\n请输入单词本名\n>>>')
        try:
            # 初始化
            f_path = '.\\%s.csv' % f_name

            if os.path.exists(f_path) == True:
                print(
                    '\n==========\n已完成初始化\n==========\n')
                CSVtool = CSVTool.Tool(f_path)
                Ori_list = CSVtool.READ()
                del Ori_list[0]  # 第一项是表头，去掉
                Wrong_list = []  # 用于存储拼错的单词的列表，参与单词重拼写
                Ori_Num = len(Ori_list)  # 总单词数
                Wrong_list_Copy = []  # 用于统计错误的单词数
                while True:
                    # 如果原单词本已默写完毕且错词本无错词则结束
                    if len(Ori_list) > 0:
                        RNum = random.choice(range(0, len(Ori_list)))
                        WordGroup = Ori_list.pop(RNum)  # 直接取出来
                        Answer = input('\nEN: %s\nZH >>> ' % WordGroup[1])
                        # 判断答案，如果错误则加入错题处
                        if Answer == WordGroup[0]:
                            print('Right✓')
                        else:
                            print('Wrong×')
                            Wrong_list.append(WordGroup)
                            Wrong_list_Copy.append(WordGroup)  # 错误单词数+1
                    elif len(Ori_list) == 0 and len(Wrong_list) > 0:
                        # 错题模式
                        print('\n=====WRONG=====\nLeft: %s\n===============' %
                              len(Wrong_list))
                        RNum = random.choice(range(0, len(Wrong_list)))
                        WordGroup = Wrong_list.pop(RNum)  # 直接取出来
                        Answer = input('\nEN: %s\nZH >>> ' % WordGroup[1])
                        # 判断答案，如果错误则加入错题处
                        if Answer == WordGroup[0]:
                            print('Right✓')
                        else:
                            print('Wrong×')
                            Wrong_list.append(WordGroup)
                    elif len(Ori_list) == 0 and len(Wrong_list) == 0:
                        Score = round((Ori_Num-len(Wrong_list_Copy)) /
                                      Ori_Num * 100, 1)
                        print('\n[{}/{}]\n你的分数: {}'.format(Ori_Num -
                                                           len(Wrong_list_Copy), Ori_Num, Score))
                        print(
                            '恭喜你! %s 的单词已经全部完成!' % f_name)
                        break
            else:
                print()('错误:没有找到单词本 %s（单词本应与本程序在同一级文件夹内）!' % f_name)
            os.system('pause')
        except:
            traceback.print_exc()


main()
