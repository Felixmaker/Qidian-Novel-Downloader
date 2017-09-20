#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Printer.py
# @Author: Felix
# @Date  : 2017/9/20
# @Desc  : Print a novel text

# 这个是在进行爬取之后，生成小说的脚本，这个可以根据你想要的内容进行定制。

import sys
import sqlite3
from Tools import informationGeter
from Tools import sql

# 这是一种处理有关字符错误的方法
reload(sys)
sys.setdefaultencoding('utf-8')

# 获取小说id，使用循环，防止错误id
while True:
    db_id = raw_input('Input the novel id: ')
    try:
        book_title = informationGeter.getIntroduction(db_id, 0)
        raw_input(('Title: ' + book_title + ' Press <enter> to continue. '))
        break
    except Exception, e:
        raw_input(e)

# 连接数据库，这应在Spider爬取对应小说后工作
conn = sqlite3.connect('Datas/novals.sqlite')
curs = conn.cursor()
print 'Connect to the database successfully.'

try:
    # 生成小说文件名
    filename = 'Novels/%s.%s.txt' % (db_id, book_title)
    # 获取数据库信息，以及文章的开头部分，并打印部分给用户
    all_number = sql.getMaxid(db_id, curs)
    text = informationGeter.getIntroduction(db_id, 1) + '\n\n'
    print 'Novel name: %s' % filename
    print 'Chapter count: %s' % all_number
except Exception, e:
    raw_input(e)
    exit()

# 生成小说的主体内容
for i in range(0, all_number):
    d = sql.getAll(db_id, curs, i)
    result_add = informationGeter.getText(d)
    text = text + '\n' + result_add
    print '{}/{}'.format(i+1, all_number)

# 写入文件
f = open(filename.decode('utf-8'), 'w')
f.write(text)
f.close()

raw_input('Successfully，the TEXT is printed in the Novels.')