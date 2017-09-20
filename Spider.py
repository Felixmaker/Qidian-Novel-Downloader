#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Spider.py
# @Author: Felix
# @Date  : 2017/9/20
# @Desc  : Spider the novels from Qidian

# 这个是用来爬取起点中文网小说的源代码，其中使用数据库储存数据
# 小说的id说明，http://book.qidian.com/info/3607314的id为3607314

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

# 连接数据库，默认在Datas文件夹下创建一个novals.sqlite的数据库
conn = sqlite3.connect('Datas/novals.sqlite')
curs = conn.cursor()
print 'Connect to the database successfully.'

# 创建表，名称默认是小说的id，如果已经存在，将询问是否重置
try:
    sql.create(db_id, curs)
except Exception, e:
    print e
    key = raw_input('Do you want to arrest this table?(y/n): ')
    if key.strip().lower() == 'y':
        sql.drop(db_id, curs)
        sql.create(db_id, curs)
    else:
        pass

# 获取小说爬取的文章数，用于断点下载小说

all_number = sql.getMaxid(db_id, curs)

# 如果没有文章在表内，all_number返回的就是一个空值，应该把这种情况考虑到

if type(all_number) != int:
    start = 0
else:
    start = all_number

# 小说文章在阅读器里面的网址前半部分，这个网址本是用于VIP用户的阅读器，但是免费小说也可以在里面阅读。
reader_url = 'http://vipreader.qidian.com/chapter/%s/' % db_id

# 写入数据库规范为一个元组，如果还想添加更多的，应该在sql.py里面的insert函数里面修改
# 本程序的写入格式为元组(下载id, 文章id, 文章标题, 文章信息, 小说的主体内容)

try:
    category_lists = informationGeter.getCategory(db_id)
    print 'Get category successfully.'
except Exception, e:
    raw_input(e)
    exit()

# 循环爬取小说的信息
# 这个过程使用Json.loads导入xhr文件的内容，这个是使用开发者工具进行获取并合理分析得到的，所要的内容其实是一个字典，对照网页取特定的值。

for i in range(start, len(category_lists)):
    d = category_lists[i]
    # 文章id，这个可能没有规律
    chapter_id = str(d['uuid']).decode('utf-8')
    # 文章标题
    chapter_title = d['cN']
    # 发布时间
    chapter_time = d['uT']
    # 点击计数
    chapter_count = str(d['cnt'])
    # 文章信息
    chapter_infor = 'Time: ' + chapter_time + '     Count: ' + chapter_count
    # 获取小说的内容
    chapter_url = str(d['id'])    # 小说文章的后半部分
    chapter_url = reader_url + chapter_url    # 小说在阅读器中的完整地址
    # 文章内容
    result = informationGeter.getContext(chapter_url)
    # 将这些信息导入数据库
    sql.insert(db_id, curs, (str(i+1), chapter_id, chapter_title, chapter_infor, result))
    conn.commit()
    print 'Spider {} successfully {}/{}'.format(chapter_id, i+1, len(category_lists))

raw_input('Successfully，Now you can run Printer.py to print a TEXT.')