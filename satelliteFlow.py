#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018-11-06 11:08
# @Author  : Yangzan
# @File    : satelliteFlow.py

import time
import pytesseract
from selenium import webdriver
from PIL import Image
import configparser
import os
import traceback
import log

def startBrowser(url, logger):
    # 浏览器设置
    logger.info('启动浏览器')
    try:
        driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        driver.maximize_window()
        logger.info('浏览器窗口最大化')
        driver.get(url)
        logger.info('进入登录网页')
    except Exception:
        logger.error('Exception occurred, check the error.log to read the detail')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)
    return driver

def search(driver, config, username, password, logger):
    url = config[0]
    xpath_username = config[1]
    xpath_password = config[2]
    xpath_verificationCodePic = config[3]
    xpath_verificationCode = config[4]
    xpath_loginButton = config[5]
    xpath_search = config[6]
    xpath_package = config[7]
    xpath_balance = config[8]
    xpath_spend = config[9]
    xpath_limit = config[10]
    xpath_logoff = config[11]
    xpath_logoffconfirm = config[12]
    pic_name_login = config[13]
    pic_name_code = config[14]
    # 输入用户名和密码
    try:
        find_username = driver.find_element_by_xpath(xpath_username)
        find_username.send_keys(username)
        time.sleep(1)
        logger.info('输入用户名完成')
        find_password = driver.find_element_by_xpath(xpath_password)
        find_password.send_keys(password)
        time.sleep(1)
        logger.info('输入密码完成')
    except Exception:
        logger.error('Exception occurred, check the error.log to read the detail')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)

    # 找出验证码
    try:
        find_verificationCodePic = driver.find_element_by_xpath(xpath_verificationCodePic)
        left = find_verificationCodePic.location['x']  # 找出验证码的位置
        top = find_verificationCodePic.location['y']
        right = find_verificationCodePic.location['x'] + find_verificationCodePic.size['width']
        bottom = find_verificationCodePic.location['y'] + find_verificationCodePic.size['height']
        logger.info('寻找验证码及确定图片大小完成')
        driver.save_screenshot(pic_name_login + '.png')  # 全屏截图
        logger.info('全屏截图并保存图片')
        im = Image.open(pic_name_login + '.png')
        im = im.crop((left, top, right, bottom))
        im.save(pic_name_code + '.png')
        logger.info('在截取的全屏图片中截取验证码图片')
        verificationCode = pytesseract.image_to_string(im)  # 识别验证码
        logger.info('验证码识别完成')
    except Exception:
        logger.error('Exception occurred when find the position of verification code')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)

    # 输入验证码并登录
    try:
        find_verificationCode = driver.find_element_by_xpath(xpath_verificationCode)
        find_verificationCode.send_keys(verificationCode)
        logger.info('输入验证码完成')
        find_login = driver.find_element_by_xpath(xpath_loginButton)
        find_login.click()
        logger.info('登录成功')
        time.sleep(1)

    except Exception:
        logger.error('Exception occurred when input the verification code')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)

    # 进入查询界面
    try:
        find_search = driver.find_element_by_xpath(xpath_search)
        find_search.click()
        time.sleep(1)
        logger.info('进入查询页面')
    except Exception:
        logger.error('Exception occurred, check the error.log to read the detail')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)

    time.sleep(2)
    package = driver.find_element_by_xpath(xpath_package).text  # 套餐
    limit = driver.find_element_by_xpath(xpath_limit).text  # 总额
    limit = float(limit[:-2])
    spend = driver.find_element_by_xpath(xpath_spend).text  # 已消费
    spend = float(spend[:-2])
    balance = driver.find_element_by_xpath(xpath_balance).text  # 剩余流量
    balance = float(balance[:-2])
    time.sleep(2)  # Let the user actually see something!
    logger.info('读取流量信息完成')
    data = []
    data.append(1)
    data.append(package)
    data.append(limit)
    data.append(spend)
    data.append(balance)

    # 注销账号
    try:
        time.sleep(1)
        find_logoff = driver.find_element_by_xpath(xpath_logoff)
        find_logoff.click()
        logger.info('准备注销账号')
        time.sleep(1)
        find_logoffconfirm = driver.find_element_by_xpath(xpath_logoffconfirm)
        find_logoffconfirm.click()
        logger.info('账号注销完成')
        # 新开一个窗口，通过执行js来新开一个窗口打开卫通登录页
        js = 'window.open("'+url+'");'
        driver.execute_script(js)
        #关闭第一个窗口
        handles = driver.window_handles
        driver.switch_to_window(handles[0])
        driver.close()
        logger.info('标签页已关闭')
        #刷新窗口信息并切换到当前的第一个标签页
        handles = driver.window_handles
        driver.switch_to_window(handles[0])
        time.sleep(1)
    except Exception:
        logger.error('Exception occurred, check the error.log to read the detail')
        traceback.print_exc(limit=None, file=open('log/error.log', 'a+'), chain=True)
    return data

def stopBrowser(driver, logger):
    time.sleep(2)
    driver.quit()
    logger.info('浏览器已退出')


