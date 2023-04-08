# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/11/05
#           Version:
#             Description:调用有道翻译api实现单词录入，用csv库存储单词并调用
# ==========================================
import youdao_translate
import CSVTool
import traceback
import os
import random
from datetime import datetime
# 复杂版本
Ver = '1.2.4_complex_Alpha'


def Model_Write():
    '''
    录入模式
    '''
    IN_Content_Dict_list = []  # 存放单词的地方
    IN_Content_list = []  # 存放单词的地方
    header_list = ["en", "zh", "Pronounce", "Example_Sentences"]  # 表头
    # 录入模式
    f_name = input('\n请输入单词/短语本名\n>>>>>>')
    # 初始化
    if '!PR' not in f_name:  # 原单词录入模式
        print('[debug]单词录入模式')
        f_path = '.\\%s.csv' % f_name
        CSVtool = CSVTool.Tool(f_path)
        # 检测单词本是否存在，若存在则追加即可
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
                    Word = youdao_translate.translate(Word_en)
                    Word_zh = Word.Get_Zh_trans()

                    Word_Pronounce = Word.Get_Pronounce()
                    if Word_Pronounce != None:
                        Word_Pronounce = '|'.join(
                            Word_Pronounce)  # 若有多个发音则用|隔开

                    Word_Example_Sentences = Word.Get_Example_Sentences()
                    if Word_Example_Sentences != None:
                        Lst_temp = []
                        for i in Word.Get_Example_Sentences():
                            Lst_temp.append(':'.join(i))
                        Word_Example_Sentences = '\n'.join(Lst_temp)
                    # 注意如果文件已经存在，则调用不同的方法，要求的输入数据格式不同
                    if os.path.exists(f_path) == True:
                        IN_Content_list.append(
                            [Word_en, Word_zh, Word_Pronounce, Word_Example_Sentences])
                    else:
                        IN_Content_Dict_list.append(
                            {'en': Word_en, 'zh': Word_zh, 'Pronounce': Word_Pronounce, 'Example_Sentences': Word_Example_Sentences})
                    print('{} - {} - {} - ✓\n{}'.format(Word_en, Word_zh,
                                                        Word_Pronounce, Word_Example_Sentences))
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
    else:  # 短语录入,只针对已有的短语，不调用api获取翻译（出错率较高）
        print('[debug]短语录入模式')
        f_path = '.\\%s.csv' % f_name
        # 检测短语本是否存在，若存在则追加即可
        if os.path.exists(f_path) == True:
            model = '追加'
        else:
            model = '新创建'
            f_path = '.\\!PR%s.csv' % f_name  # 新创建的本子在前面加上识别号 !PR 以便下次追加时可以识别出来

        CSVtool = CSVTool.Tool(f_path)
        print(
            '\n==========\n已完成初始化\n模式:%s\n==========\n请输入需要录入的短语(输入 /finish 来完成录入)' % model)
        while True:
            Phrase_en = input('短语（英文）>>>')
            Phrase_zh = input('短语（中文）>>>')
            Phrase_Pronounce = None  # 短语发音暂不支持，此处仅用于兼容单词本格式
            Phrase_Example_Sentences = input('例句 >>>').replace(
                ', ', '，')  # 由于csv文件用英文逗号做数据分界，若例句中有英文逗号会影响分界导致例句显示不全
            if Word_en != '/finish':
                try:  # 有可能出现录入错误,若此单词录入错误就报错，然后继续
                    # 注意如果文件已经存在，则调用不同的方法，要求的输入数据格式不同
                    if os.path.exists(f_path) == True:
                        IN_Content_list.append(
                            [Phrase_en, Phrase_zh, Phrase_Pronounce, Phrase_Example_Sentences])
                    else:
                        IN_Content_Dict_list.append(
                            {'en': Phrase_en, 'zh': Phrase_zh, 'Pronounce': Phrase_Pronounce, 'Example_Sentences': Phrase_Example_Sentences})
                    print('{} - {} - {} - ✓\n{}'.format(Phrase_en, Phrase_zh,
                                                        Phrase_Pronounce, Phrase_Example_Sentences))
                except:
                    traceback.print_exc()
                    pass
            else:
                break
        # 注意如果文件已经存在就不再重复写入
        if os.path.exists(f_path) == True:  # 存在
            CSVtool.ADD(IN_Content_list)
            print('[追加]短语本名:{} - 写入 - ✓'.format(f_name+'.csv'))
        else:  # 不存在
            CSVtool.WRITE(header_list, IN_Content_Dict_list)
            CSVtool.ADD(IN_Content_list)
            print(
                '[新创建]短语本名:{} - 写入 - ✓\nTip:单词本已创建在本程序的同级文件夹内，除删除之外请勿随意移动此文件'.format('!PR'+f_name+'.csv'))
        os.system('pause')


def Model_Recite():
    '''
    背诵模式
    '''
    # 背诵模式
    f_name = input('\n请输入单词/短语本名\n>>>')
    try:
        # 初始化
        f_path = '.\\%s.csv' % f_name

        if os.path.exists(f_path) == True:
            print(
                '\n==========\n已完成初始化\n==========\n')

            CSVtool = CSVTool.Tool(f_path)
            Ori_list = CSVtool.READ()
            del Ori_list[0]  # 第一项是表头，不要了
            Wrong_list = []  # 用于存储拼错的单词/短语的列表，参与单词/短语重拼写
            Ori_Num = len(Ori_list)  # 总单词数
            print('共有%s个单词/短语' % Ori_Num)
            Wrong_list_Copy = []  # 用于统计错误的单词数
            while True:
                # 如果原单词/短语本已默写完毕且错词本无错词则结束
                if len(Ori_list) > 0:
                    RNum = random.choice(range(0, len(Ori_list)))
                    WordGroup = Ori_list.pop(RNum)  # 直接取出来
                    Answer = input('\nZH: %s\n EN>>> ' % WordGroup[1])
                    # 判断答案，如果错误则加入错题处
                    if Answer == WordGroup[0]:
                        print('Right✓')
                        if len(WordGroup) >= 4:
                            print('-----\nProunce: %s\nExample Sentences:%s\n-----\n' %
                                  (WordGroup[2], WordGroup[3]))
                    elif Answer == '/left':  # 2023/03/29 15:37:10 ➕显示剩余单词数
                        print('Left: %s' % len(Ori_list))  # 显示剩余单词数
                        Ori_list.append(WordGroup)  # 将单词放回待测试列表

                    else:
                        print('Wrong×')
                        Wrong_list.append(WordGroup)
                        Wrong_list_Copy.append(WordGroup)  # 错误单词/短语数+1
                elif len(Ori_list) == 0 and len(Wrong_list) > 0:
                    # 错题模式
                    print('\n=====WRONG=====\nLeft: %s\n===============' %
                          len(Wrong_list))
                    RNum = random.choice(range(0, len(Wrong_list)))
                    WordGroup = Wrong_list.pop(RNum)  # 直接取出来
                    Answer = input('\nZH: %s\n EN>>> ' % WordGroup[1])
                    # 判断答案，如果错误则加入错题处
                    if Answer == WordGroup[0]:
                        print('Right✓')
                        # 新版本则把读音和例句也打印出来
                        if len(WordGroup) >= 4:
                            print('-----\nProunce: %s\nExample Sentences:%s\n-----\n' %
                                  (WordGroup[2], WordGroup[3]))
                    elif Answer == '/save':  # 将错题本保存下来
                        header = {'en', 'zh', 'Pronounce', 'Example_Sentences'}
                        # 2023/03/14 21:41:18 ➕错题本文件名含时间，便于辨认
                        SaveTime = str(datetime.today()).split(
                            '.')[0].replace(' ', '-').replace(':', '-')
                        CSVTool.Tool('./Wrong-%s-%s-%s.csv' %
                                     (len(Wrong_list_Copy), f_name, SaveTime)).WRITE(header, {})
                        CSVTool.Tool(
                            './Wrong-%s-%s-%s.csv' % (len(Wrong_list_Copy), f_name, SaveTime)).ADD(Wrong_list_Copy)
                        print('[debug]错题已保存至./Wrong-%s-%s-%s.csv' %
                              (len(Wrong_list_Copy), f_name, SaveTime))
                        Wrong_list.append(WordGroup)
                    # 2023/04/02 08:30:43 ➕将剩余错误的单词显示出来
                    elif Answer == '/show':
                        if len(Wrong_list) > 0:
                            a = 1
                            # 记得把取出来的那个单词加回去
                            Wrong_list.append(WordGroup)
                            for i in Wrong_list:
                                print('\nNo.%s\nen:%s,zh:%s %s\n%s' %
                                      (a, i[0], i[1], i[2], i[3]))
                                print()
                                a += 1
                        else:
                            print('[debug]剩余单词显示错误！')

                    else:
                        print('Wrong×')
                        Wrong_list.append(WordGroup)
                elif len(Ori_list) == 0 and len(Wrong_list) == 0:
                    Score = round((Ori_Num-len(Wrong_list_Copy)) /
                                  Ori_Num * 100, 1)
                    print('\n[{}/{}]\n你的分数: {}'.format(Ori_Num -
                                                       len(Wrong_list_Copy), Ori_Num, Score))
                    print(
                        '恭喜你! %s 的单词/短语已经全部完成!' % f_name)
                    break
        else:
            print('错误:没有找到单词/短语本 %s（单词/短语本应与本程序在同一级文件夹内）!' % f_name)
        os.system('pause')
    except:
        traceback.print_exc()


def Model_Transform():
    '''
    转换模式
    将简便模式的单词本转为复杂模式单词本
    '''


def Model_Split():
    '''
    切片模式
    将复杂模式单词本中的单词切割成特定数量的单词本，
        便于背诵
    '''
    # 背诵模式
    f_name = input('\n请输入单词/短语本名\n>>>')
    try:
        # 初始化
        f_path = '.\\%s.csv' % f_name

        if os.path.exists(f_path) == True:
            print(
                '\n==========\n已完成初始化\n==========\n')

            CSVtool = CSVTool.Tool(f_path)
            Ori_list = CSVtool.READ()
            Ori_header = Ori_list[0]  # 储存表头，分片完每个单词本都需要加入
            del Ori_list[0]  # 第一项是表头，不要了
            Ori_Num = len(Ori_list)  # 总单词数
            print('共有%s个单词/短语\n' % Ori_Num)

            Split_num = int(input('\n需要切割成几部分？\n>>>'))
            Signal_num = len(Ori_list)//Split_num

            for i in range(1, Split_num+1):
                if i != Split_num:  # 不是最后一部份
                    CSVtool_S = CSVTool.Tool(
                        './%s_%s_%s.csv' % (f_name, Signal_num, i))
                    CSVtool_S.WRITE(Ori_header, [{'en': i[0], 'zh': i[1],
                                                  'Pronounce': i[2], 'Example_Sentences': i[3]}
                                                 for i in Ori_list[(i-1)*Signal_num:i*Signal_num]])
                else:  # 最后一部份
                    CSVtool_S = CSVTool.Tool(
                        './%s_%s_%s.csv' % (f_name, Signal_num, i))
                    CSVtool_S.WRITE(Ori_header, [{'en': i[0], 'zh': i[1],
                                                  'Pronounce': i[2], 'Example_Sentences': i[3]}
                                                 for i in Ori_list[(i-1)*Signal_num:]])

            print('[debug]切片对象:%s 丨切片数: %s 切片完毕✓' % (f_name, Split_num))

        else:
            print('错误:没有找到单词/短语本 %s（单词/短语本应与本程序在同一级文件夹内）!' % f_name)
        os.system('pause')
    except:
        traceback.print_exc()


def main():
    print('WordsReciteTool %s Service Start' % Ver)
    while True:
        CMD = input('R/W/S ?\nTip:输入R进入背诵模式,W进入录入模式,S进入切片模式\n>>>')
        if CMD == 'W':
            Model_Write()
        elif CMD == 'R':
            Model_Recite()
        elif CMD == 'S':
            Model_Split()
        elif CMD == '/exit':
            break


main()
