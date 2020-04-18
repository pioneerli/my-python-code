#!/bin/env python3
# -*- coding:UTF-8 -*-
# _author:kaliarch
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.cvm.v20170312 import cvm_client, models
import configparser
import time
import os
import logging
class CvmOper():
    def __init__(self,logger):
        config = configparser.ConfigParser()
        config.read('config.py',encoding='utf-8')
        self.instance_list = config['common']['InstanceIds'].split(',')
        print(self.instance_list)
        cred = credential.Credential(config['common']['SecretId'], config['common']['SecretKey'])
        self.clentoper = cvm_client.CvmClient(cred, config['common']['Region'])

        self.logger = logger
        self.logger.info("------------------------start cvm of API log-------------")
    def reboot_instance(self):
        """
        重启cvm
        :return:
        """
        # 设置参数
        request = models.RebootInstancesRequest()
        request.InstanceIds=self.instance_list
        # 发起请求
        response = self.clentoper.RebootInstances(request)
        self.logger.info("public ecs vpn reboot successful!")
        self.logger.info(response.to_json_string())
        print(response.to_json_string())

    def start_instance(self):
        """
        启动cvm
        :return:
        """
        request = models.StartInstancesRequest()
        request.InstanceIds = self.instance_list
        # 发起请求
        response = self.clentoper.StartInstances(request)
        self.logger.info("public ecs vpn reboot successful!")
        self.logger.info(response.to_json_string())
        print(response.to_json_string())

    def stop_instance(self):
        """
        停止cvm
        :return:
        """
        request = models.StopInstancesRequest()
        request.InstanceIds = self.instance_list
        # 发起请求
        response = self.clentoper.StopInstances(request)
        self.logger.info("public ecs vpn reboot successful!")
        self.logger.info(response.to_json_string())
        print(response.to_json_string())

    def testlog(self):
        self.logger.info("public test log")

class CvmLog:
    def __init__(self,filename):
        self.filename = filename
    def createDir(self):
        _LOGDIR = os.path.join(os.path.dirname(__file__), 'cvmlog')
        print(_LOGDIR)
        _TIME = time.strftime('%Y-%m-%d', time.gmtime()) + '-'
        _LOGNAME = _TIME + self.filename
        print(_LOGNAME)
        LOGFILENAME = os.path.join(_LOGDIR, _LOGNAME)
        print(LOGFILENAME)
        if not os.path.exists(_LOGDIR):
            os.mkdir(_LOGDIR)
        return LOGFILENAME


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
    cvmloger = CvmLog('cvm-oper.log')
    logfilename = cvmloger.createDir()
    logger = cvmloger.createlogger(logfilename)
    # 生成app对象
    app = CvmOper(logger)
    # 启动服务
    # app.start_instance()
    # 停止实例
    # app.stop_instance()
    # 重启实例
    app.reboot_instance()

