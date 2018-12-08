#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-11-07 9:59
# @Author  : Yangzan
# @File    : database.py
import pymysql
import traceback
import configparser

def DBconnect(host, user, passwd, db, port, charset):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port,
                           charset=charset)
    return conn

def DBclose(conn, cur):
    cur.close()
    conn.close()

