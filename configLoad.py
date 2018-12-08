#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-11-08 11:46
# @Author  : Yangzan
# @File    : configLoad.py
import os
import configparser
import traceback


def getConfig(logger):
    # --------------------------读取配置文件------------------------#
    # 拼接配置文件路径
    logger.info('开始读取配置文件信息')
    localPath = os.getcwd()
    configPath = os.path.join(localPath, 'config/config.conf')
    configPath = os.path.abspath(configPath)
    # 获取配置文件信息
    configFile = configparser.ConfigParser()
    configFile.read(configPath, encoding='UTF-8')
    logger.info('配置文件载入完成')

    # 参数读取：
    try:
        # 网页相关参数
        url = configFile.get("login", "loginUrl")
        xpath_username = configFile.get("xpath", "xpath_username")
        xpath_password = configFile.get("xpath", "xpath_password")
        xpath_verificationCodePic = configFile.get("xpath", "xpath_verificationCodePic")
        xpath_verificationCode = configFile.get("xpath", "xpath_verificationCode")
        xpath_loginButton = configFile.get("xpath", "xpath_loginButton")
        xpath_search = configFile.get("xpath", "xpath_search")
        xpath_package = configFile.get("xpath", "xpath_package")
        xpath_balance = configFile.get("xpath", "xpath_balance")
        xpath_spend = configFile.get("xpath", "xpath_spend")
        xpath_limit = configFile.get("xpath", "xpath_limit")
        xpath_logoff = configFile.get("xpath", "xpath_logoff")
        xpath_logoffconfirm = configFile.get("xpath", "xpath_logoffconfirm")
        # 数据库相关参数
        dbhost = configFile.get("database", "host")
        dbport = configFile.getint("database", "port")
        db = configFile.get("database", "db")
        dbuser = configFile.get("database", "username")
        dbpasswd = configFile.get("database", "passwd")
        dbcharset = configFile.get("database", "charset")
        # 设置图片文件名
        pic_name_login = 'loginPic'
        pic_name_code = 'codePic'
        config = [url, xpath_username, xpath_password, xpath_verificationCodePic, xpath_verificationCode,
                  xpath_loginButton,
                  xpath_search, xpath_package, xpath_balance, xpath_spend, xpath_limit, xpath_logoff,
                  xpath_logoffconfirm,
                  pic_name_login, pic_name_code, dbhost, dbport, db, dbuser, dbpasswd, dbcharset]
        return config
    except Exception:
        logger.error('Exception occurred, check the error.log to read the detail')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)
        logger.info('配置文件信息读取完毕')
