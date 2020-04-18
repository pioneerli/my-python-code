#!/bin/env python3
# -*- coding:UTF-8 -*-
# _author:kaliarch
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import RebootInstanceRequest,StartInstanceRequest,StopInstanceRequest
import time
import os
import logging
class ecsOper():
    def __init__(self,logger):
        self.clentoper = client.AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')
        self.logger = logger
        self.logger.info("------------------------start reboot vpn ecs of API log-------------")
    def reboot_instance(self):
        # 设置参数
        request = RebootInstanceRequest.RebootInstanceRequest()
        request.set_accept_format('json')
        request.add_query_param('InstanceId', 'i-bjk23j1rlvfghlq79au')
        # 发起请求
        response = self.clentoper.do_action_with_exception(request)
        self.logger.info("public ecs vpn reboot successful!")
        self.logger.info(response)
        print(response)

    def start_instance(self):
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_accept_format('json')
        request.add_query_param('InstanceId', 'i-bjk23j1rlvfghlq79au')
        # 发起请求
        response = self.clentoper.do_action_with_exception(request)
        self.logger.info("public ecs vpn start successful!")
        self.logger.info(response)
        print(response)

    def stop_instance(self):
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_accept_format('json')
        request.add_query_param('InstanceId', 'i-bjk23j1rlvfghlq79au')
        request.add_query_param('ForceStop', 'false')
        # 发起请求
        response = self.clentoper.do_action_with_exception(request)
        self.logger.info(response)
        print(response)

    def testlog(self):
        self.logger.info("public test log")

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

if __name__ == "__main__":
    glploger = Glp_Log('public-vpn.log')
    logfilename = glploger.createDir()
    logger = glploger.createlogger(logfilename)

    app = ecsOper(logger)
    app.reboot_instance()

