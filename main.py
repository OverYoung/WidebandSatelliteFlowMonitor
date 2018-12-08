#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-11-08 11:18
# @Author  : Yangzan
# @File    : main.py

import time
import log
import traceback
import configLoad
import satelliteFlow
import database

#初始化log对象
logger = log.myLogger('log')
logger.info('程序启动')

localtime = time.localtime(time.time())
localhour = localtime.tm_hour
localmin = localtime.tm_min
localsec = localtime.tm_sec
#每六小时进行一次查询
while True:
    #只有整点进行查询
    if localhour % 11 == 0 and localmin == 21 and localsec >=0 and localsec <=50:
        # 读取配置文件信息
        config = configLoad.getConfig(logger)
        print(config)
        dbhost = config[15]
        dbport = config[16]
        db = config[17]
        dbuser = config[18]
        dbpasswd = config[19]
        dbcharset = config[20]
        url = config[0]

        # 启动浏览器
        driver = satelliteFlow.startBrowser(url, logger)

        accountNum = 0
        accountusername = []
        accountpassword = []
        #从数据库获取卫通的账号
        try:
            dbConn = database.DBconnect(dbhost, dbuser, dbpasswd, db, dbport, dbcharset)
            logger.info('连接数据库完成')
            dbCur = dbConn.cursor()
            sql = "SELECT `id`, `username`, `password` FROM Account;"
            dbCur.execute(sql)
            dbConn.commit()
            account = dbCur.fetchall()
            accountNum = dbCur.rowcount
            for num in range(0, accountNum):
                accountusername.append(account[num][1])
                accountpassword.append(account[num][2])
            database.DBclose(dbConn, dbCur)
            logger.info('与数据库断开连接')
        except Exception:
            logger.error('Exception occurred, check the error.log to read the detail')
            traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)
            logger.error('发生错误，终止本次循环')
            continue

        #循环获取每一个账号的流量情况
        for num in range(0, accountNum):
            username = accountusername[num]
            password = accountpassword[num]
            #流量情况获取
            data = satelliteFlow.search(driver, config, username, password, logger)
            #print(data)
            #插入数据至数据库
            try:
                dbConn = database.DBconnect(dbhost, dbuser, dbpasswd, db, dbport, dbcharset)
                logger.info('连接数据库完成')
                dbCur = dbConn.cursor()
                sql = "insert into Flow(`accountId`, `package`, `limit`, `spend`, `balance`) values(%s, %s, %s, %s, %s);"
                try:
                    dbCur.execute(sql, data)
                    dbConn.commit()
                    logger.info('数据插入完成')
                except Exception:
                    # 发生错误进行回滚
                    dbConn.rollback()
                database.DBclose(dbConn, dbCur)
                logger.info('与数据库断开连接')
            except Exception:
                logger.error('Exception occurred, check the error.log to read the detail')
                traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)
                logger.error('发生错误，终止本次循环')
                continue
    else:
        print('未达到查询执行条件：每六小时准点执行一次')
        pass
    #更新时间
    localtime = time.localtime(time.time())
    localhour = localtime.tm_hour
    localmin = localtime.tm_min
    localsec = localtime.tm_sec

    #还需要添加邮件提醒