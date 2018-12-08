#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-11-07 10:58
# @Author  : Yangzan
# @File    : log.py
import logging
import datetime
import logging.handlers

class myLogger():
    #-----------------初始化日志类------------------#
    def __init__(self, loggerName):
        #创建一个logger
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)
        #创建一个handler用于写入所有级别的日志,使用TimedRotatingFileHandler可以实现日志按天进行切割
        handler_all = logging.handlers.TimedRotatingFileHandler('log/all.log', when='midnight', interval=1,
                                                                backupCount=7, encoding='utf-8',
                                                                atTime=datetime.time(0, 0, 0, 0))
        handler_all.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        #创建一个handler，用于写入Error级别的日志
        handler_error = logging.FileHandler('log/error.log', encoding='utf-8')
        handler_error.setLevel(logging.ERROR)
        handler_error.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

        self.logger.addHandler(handler_all)
        self.logger.addHandler(handler_error)
    # ----------------------------------------------#

    #-----------------插入不同类型的日志------------------#
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)