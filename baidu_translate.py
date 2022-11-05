# python爬虫实现百度翻译
# urllib和request POST参数提交
# 缺少包请自行查看之前的笔记

from urllib import request, parse
import json


def translate(word):
    base_url = 'https://fanyi.baidu.com/sug'

    # 构建请求对象
    data = {
        'kw': word
    }
    # 编码工作使用urllib.parse的urlencode()函数，
    #   帮我们将key:value这样的键值对转换成"key=value"这样的字符串，
    #       解码工作可以使用urllib.parse的unquote()函数。
    data = parse.urlencode(data)

    # 模拟浏览器
    header = {"User-Agent": "mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}

    req = request.Request(url=base_url, data=bytes(
        data, encoding='utf-8'), headers=header)
    res = request.urlopen(req)

    # 获取响应的json字符串
    str_json = res.read().decode('utf-8')
    # 把json转换成字典
    myjson = json.loads(str_json)
    info = myjson['data'][0]['v']
    # print(info)
    return info


def main_handler(event, content):
    print('Baidu_translate Service started')
    While = 1
    while While >= 1:
        word = input('请输入翻译的单词：')
        if word == '/exit':
            print("感谢使用百度翻译！")
            break
        else:
            translate(word)
