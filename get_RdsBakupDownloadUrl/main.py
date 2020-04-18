#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

from get_rdsinfo import rdsOper
from set_log import rdsLog


def init_log():
    """
    init logger
    :return: logger
    """
    logoper = rdsLog()
    filename = logoper.create_dir()
    rdslog = logoper.create_logger(filename)
    return rdslog

def app_rdsbak():
    """

    :return:
    """
    log = init_log()
    rdsapp = rdsOper(log)
    result = rdsapp.des_instance()
#    print(rdsapp.get_rdsdownload_url(result, 'BackupIntranetDownloadURL'))
    print(rdsapp.get_rdsdownload_url(result, 'BackupDownloadURL'))

if __name__ == "__main__":
    app_rdsbak()
