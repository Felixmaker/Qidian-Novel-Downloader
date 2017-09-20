#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sql.py
# @Author: Felix
# @Date  : 2017/9/17
# @Desc  : Sql commands

import sqlite3

# id为小说id，curs为游标位置

def create(id, curs):
    create = 'CREATE TABLE "%s" (download_id INTEGER, id TEXT, chapter TEXT, information TEXT, context TEXT)' % id
    curs.execute(create)
    print 'Create table successfully.'

def drop(id, curs):
    drop = 'DROP TABLE "main"."%s"' % id
    curs.execute(drop)
    print 'Drop table successfully.'

def insert(id, curs, things):
    insert = 'INSERT INTO "%s" (download_id, id, chapter, information, context) VALUES (?, ?, ?, ?, ?)' % id
    curs.execute(insert, things)

def getMaxid(id, curs):
    max_id = 'SELECT MAX(download_id) FROM "%s"' % id
    curs.execute(max_id)
    all_number = curs.fetchall()[0][0]
    return all_number

def getAll(id, curs, i):
    get = 'SELECT * FROM "{}" WHERE download_id = {}'.format(id, i+1)
    curs.execute(get)
    d = curs.fetchall()[0]
    return d