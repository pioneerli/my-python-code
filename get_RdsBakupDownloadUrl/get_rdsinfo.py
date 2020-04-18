#!/bin/env python
# -*- coding:utf-8 -*-
# _author:kaliarch

from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeBackupsRequest
import json
import datetime
import configparser


class rdsOper():
    def __init__(self,logger):
        """
        defined start and end time
        init clentoper
        """
        configoper = configparser.ConfigParser()
        configoper.read('info.conf')
        self.accessKeyId = configoper['akconfig']['accessKeyId']
        self.accessSecret = configoper['akconfig']['accessSecret']
        self.region = configoper['akconfig']['region']
        self.instanceId = configoper['akconfig']['instanceId']
        self.BackupMode = configoper['akconfig']['BackupMode']
        self.BackupDownURL = configoper['akconfig']['BackDownloadURL']
        self.clent_oper = client.AcsClient(self.accessKeyId, self.accessSecret, self.region)
        self.start_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d") + 'T00:00Z'
        self.end_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d") + 'T23:59Z'
        self.logger = logger

    def des_instance(self):
        """
        set param
        :return: response
        """
        request = DescribeBackupsRequest.DescribeBackupsRequest()
        request.set_accept_format('json')
        # DBInstanceId:
        request.add_query_param('DBInstanceId', self.instanceId)
        # StartTime:
        request.add_query_param('StartTime', self.start_time)
        # EndTime:
        request.add_query_param('EndTime', self.end_time)
        # BackupId:
        # request.add_query_param('BackupId', '备份集ID')
        # BackupStatus:
        request.add_query_param('BackupStatus', 'Success')
        # 备份类型，取值范围:Automated：常规任务
        request.add_query_param('BackupMode', self.BackupMode)
        response = self.clent_oper.do_action_with_exception(request)
        self.logger.info("init request complate!")
        return response

    # 接受响应，定义外网或内网url,公网：BackupDownloadURL，内网：BackupIntranetDownloadURL
    def get_rdsdownload_url(self, response, net_type='BackupDownloadURL'):
        """
        :param response:
        :param net_type:
        :return: rds_download_url
        """
        context = json.loads(response.decode('utf-8'))
        con_list = context['Items']['Backup']
        net_type = self.BackupDownURL
        try:
            download_url = con_list[0][net_type]

            log_url = str(datetime.datetime.now()) +" downloadurl:"+ download_url
            self.logger.info(log_url)
        except Exception as e:
            self.logger.info(e)
            exit()
        return download_url

