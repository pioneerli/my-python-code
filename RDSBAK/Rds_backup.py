#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import CreateBackupRequest
import time
import os
import logging

class rdsOper():
    def __init__(self,logger):
        self.clentoper = client.AcsClient('LTAIhfXlcjyl****','GwfAM344K2ELm345184356TVgRfAso','cn-shanghai')
        self.logger = logger
        self.logger.info("------------------------start exec rds backup API log-------------")
    def backup_instance(self):
        # 设置参数
        request = CreateBackupRequest.CreateBackupRequest()
        request.set_accept_format('json')
        request.add_query_param('DBInstanceId', 'rm-uf6x**5u1x842y61y')

        #如果为单库备份，可以添加DBName
        # request.add_query_param('DBName', 'mydb')

        #BackupMethod为备份方式：Logical：逻辑备份，Physical：物理备份
        request.add_query_param('BackupMethod', 'Physical')
        #BackupType为备份类型： Auto：自动计算是全量备份还是增量备份；FullBackup：全量备份。默认值为Auto。
        request.add_query_param('BackupType', 'Auto')

        response = self.clentoper.do_action_with_exception(request)
        self.logger.info("rdsbackup mission submission successful!")
        self.logger.info(response)
        print(response)


class Rds_Log:
    def __init__(self,filename):
        self.filename = filename
    def createDir(self):
        _LOGDIR = os.path.join(os.path.dirname(__file__), 'rdsbackuplog')
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
    glploger = Rds_Log('rdsbackup.log')
    logfilename = glploger.createDir()
    logger = glploger.createlogger(logfilename)

    app = rdsOper(logger)
    app.backup_instance()


