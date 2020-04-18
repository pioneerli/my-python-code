#!/bin/env python3
from pyvirtualdisplay import Display
from selenium import webdriver
import time
import os
import logging

class Glp_SangFor:
    def __init__(self,logger):
        self.logger = logger
        self.logger.info("--------------start log----------------")
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.browser = webdriver.Firefox()
        self.logger.info("start browser successfuly")
        self.sangfor_url = "深信服url"
        self.username = '深信服用户名'
        self.password = '深信服密码'

    def login(self):
        self.browser.get(self.sangfor_url)
        self.browser.implicitly_wait(5)
        self.browser.find_element_by_name('user').send_keys(self.username)
        self.browser.find_element_by_name('password').send_keys(self.password)
        self.browser.find_element_by_class_name('buttons').click()
        self.browser.implicitly_wait(5)
        self.logger.info("loggin sangfor successfuly")

    def client_reboot(self):
        self.browser.find_element_by_id("ext-gen111").click()
        print(self.browser.find_element_by_id("ext-gen111").text)
        self.browser.implicitly_wait(15)
        time.sleep(60)
        self.logger.info("switch mainiframe start")
        try:
            print(self.browser.find_element_by_link_text("重启/重启服务/关机").text)
            self.browser.find_element_by_link_text("重启/重启服务/关机").click()
            self.browser.implicitly_wait(3)
            self.browser.switch_to_frame("mainiframe")
            self.browser.implicitly_wait(8)
            time.sleep(10)
            self.browser.find_element_by_xpath("//button[@id='ext-gen19']").click()
            print(self.browser.find_element_by_xpath("//button[@id='ext-gen19']").text)
            self.browser.implicitly_wait(10)
            #self.browser.find_element_by_xpath("//button[@id='ext-gen42']").click()
            print(self.browser.find_element_by_xpath("//button[@id='ext-gen42']").text)
        except Exception as e:
            self.logger.exception("reboot successful")
            return 1
        self.browser.close()
        self.logger.info("browser close successful")
        self.logger.info("--------------end log----------------")
        return 0

class Glp_Log:
    def __init__(self,filename):
        self.filename = filename
    def createDir(self):
        _LOGDIR = os.path.join(os.path.dirname(__file__), 'publiclog')
        print(_LOGDIR)
        _TIME = time.strftime('%Y-%m-%d', time.gmtime()) + '-'
        _LOGNAME = _TIME + self.filename
        print(_LOGNAME)
        LOGFILENAME = os.path.join(_LOGDIR, _LOGNAME)
        print(LOGFILENAME)
        if not os.path.exists(_LOGDIR):
            os.mkdir(_LOGDIR)
        return LOGFILENAME
        print(LOGFILENAME)

    def createlogger(self,logfilename):
        logger= logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logfilename)
        handler.setLevel(logging.INFO)
        formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formater)
        logger.addHandler(handler)
        return logger

if __name__ == '__main__':
    os.system("pkill firefox")
    os.system("pkill Xvfb")
    glploger = Glp_Log('public-vpn.log')
    logfilename = glploger.createDir()
    logger = glploger.createlogger(logfilename)

    sangfor_oper = Glp_SangFor(logger)
    sangfor_oper.login()
    sangfor_oper.client_reboot()
