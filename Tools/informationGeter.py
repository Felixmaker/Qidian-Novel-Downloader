#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : informationGeter.py
# @Author: Felix
# @Date  : 2017/9/17
# @Desc  : Get information

import urllib2
import json
import re

def getIntroduction(id, x):
    'Get the novel name. \n(id, x) x = 0 --> verification x = 1 --> preface'

    url = 'http://book.qidian.com/info/' + id
    html = urllib2.urlopen(url).read()

    # 获取小说的信息
    book_info = re.findall(r'<div class="book-info ">(.*?)</div>', html, re.S)[0]

    book_title = re.findall(r'<h1><em>(.*?)</em><span><a class="writer"', book_info, re.S)[0]
    book_author = re.findall(r'data-eid="qd_G08">(.*?)<', book_info, re.S)[0]
    book_small = re.findall(r'<p class="intro">(.*?)</p>', book_info, re.S)[0].strip()

    # 获取小说的序言
    book_intro = re.findall(r'<div class="book-intro">(.*?)</div>', html, re.S)[0]
    book_preface = re.findall(r'<p>(.*?)</p>', book_intro, re.S)[0].strip().split('<br>')
    # 获取的序言是分段的，下面将他们合成
    result = ''
    for i in range(len(book_preface)):
        result = result + book_preface[i] + '\n'

    # 生成Spider里面的验证部分
    verification = book_title
    # 生成小说的开头部分
    preface = '小说: ' + book_title + '\n\n' + '作者: ' + book_author + '\n\n' + '简介: ' + book_small + '\n\n' + result

    get = (verification, preface)[x]
    return get

# 用来获取小说的目录，并返回目录列表，列表里面的元素包含很多信息，将用于后期数据库写入作业。
def getCategory(id):
    'Get the category.'
    url = 'http://book.qidian.com/ajax/book/category?_csrfToken=YeI5xwwlXv82Lg6bU5sBNF7gWXJXZYktv3AP58l2&bookId=%s' % id
    html = urllib2.urlopen(url).read()
    li = json.loads(html)['data']['vs']
    category_lists = []
    for i in li:
        category_lists = category_lists + i['cs']
    return category_lists

# 按照一定的规范获取阅读器中文章的内容
def getContext(chapter_url):
    'Get the context.'
    chapter_html = urllib2.urlopen(chapter_url).read().decode('utf-8')
    context = re.findall(r'<div class="read-content j_readContent">(.*?)</div>', chapter_html, re.S)[0]
    tage_p = re.findall(r'<p>(.*?)<', context, re.S)
    result = ''
    for i in range(0, len(tage_p)):
        result = result + tage_p[i].strip() + '\n'
    return result
# 按照一定的规范获取数据库里面的信息，生成文本的主体部分
def getText(d):
    'get the body of the text.'
    result = ''
    for i in range(1, 5):
        result = result + d[i] + '\n\n'
    return result