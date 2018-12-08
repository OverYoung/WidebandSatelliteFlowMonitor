#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-11-09 11:18
# @Author  : Yangzan
# @File    : main.py

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import os
import traceback
import configparser

def getMailConfig(logger):
    # --------------------------读取配置文件------------------------#
    try:
        # 拼接配置文件路径
        logger.info('开始读取配置文件信息')
        localPath = os.getcwd()
        configPath = os.path.join(localPath, 'config/config.conf')
        configPath = os.path.abspath(configPath)
        # 获取配置文件信息
        configFile = configparser.ConfigParser()
        configFile.read(configPath)
        logger.info('配置文件载入完成')
        mailConfig = []
        mailConfig.append(configFile.get("mail", "mail_username"))
        mailConfig.append(configFile.get("mail", "mail_password"))
        mailConfig.append(configFile.get("mail", "smtp_server"))
        return mailConfig
    except Exception:
        logger.error('Exception occurred, check the error.log to read the detail')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, encoders.unicode) else addr))

from_addr = ''
password = ''
to_addr = 'yangzan@mail.bdsmc.net'
smtp_server = ''

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = Header("菜鸟教程", 'utf-8')
msg['To'] = Header("测试", 'utf-8')
msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()