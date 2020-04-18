#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

import configparser
import time
import json
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import CreateImageRequest
from aliyunsdkecs.request.v20140526 import CopyImageRequest
from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
import logger


class EcsOper():
    def __init__(self,logger):
        """
        初始化获取系config信息，配置日志
        :param logger:
        """
        config = configparser.ConfigParser()
        config.read('config.cfg',encoding='utf-8')
        accessKeyId = config['common']['accessKeyId']
        accessSecret = config['common']['accessSecret']
        self.s_RegionId = config['source']['s_RegionId']
        self.s_InstanceId_list = config['source']['s_InstanceId']
        self.s_ImageName = config['source']['s_ImageName']
        self.s_Description = config['source']['s_Description']

        self.d_DestinationRegionId = config['destination']['d_DestinationRegionId']
        self.d_DestinationImageName = config['destination']['d_DestinationImageName']
        self.d_DestinationDescription = config['destination']['d_DestinationDescription']
        self.ecshelper = client.AcsClient(accessKeyId,accessSecret,self.s_RegionId)

        logger = logger.LogHelper()
        logname = logger.create_dir()
        self.logoper = logger.create_logger(logname)

    # 创建实例生成器
    def _get_Instance(self):
        for Instance in self.s_InstanceId_list.split(','):
            yield Instance

    # 镜像制作
    def _create_image(self,s_InstanceId):
        """
        创建镜像
        :return:返回镜像id
        """
        s_timer = time.strftime("%Y-%m-%d-%H:%M", time.localtime(time.time()))
        request = CreateImageRequest.CreateImageRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId', self.s_RegionId)
        request.add_query_param('InstanceId', s_InstanceId)
        request.add_query_param('ImageName', self.s_ImageName + s_timer)
        request.add_query_param('Description', self.s_Description + s_timer)
        response = self.ecshelper.do_action_with_exception(request)
        self.logoper.info('创建镜像任务已提交,镜像id:%s' % json.loads(response)["ImageId"])
        print('实例%s,创建镜像任务已提交,镜像id:%s' % (s_InstanceId,json.loads(response)["ImageId"]))
        return json.loads(response)["ImageId"]

    # 查询镜像状态
    def _describe_image(self,imageid):
        """
        查询image状态
        :param imageid:
        :return:
        """
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId', self.s_RegionId)
        request.add_query_param('ImageId', imageid)
        response = self.ecshelper.do_action_with_exception(request)
        # 进度 json.loads(response)['Images']['Image'][0]['Progress']
        self.logoper.info('镜像创建进度:%s' %json.loads(response)['Images']['Image'][0]['Progress'])
        # 镜像状态
        return json.loads(response)['Images']['Image'][0]['Status']

    #镜像复制
    def _copy_image(self,imageid):
        """
        镜像复制
        :param imageid:源镜像id
        :return: 复制成功后的镜像id
        """
        flag = True
        while flag:
            try:
                if self._describe_image(imageid) == 'Available':
                    flag = False
                else:
                    time.sleep(300)
            except Exception as e:
                pass
        print('镜像已经创建完成')
        d_timer = time.strftime("%Y-%m-%d-%H:%M", time.localtime(time.time()))
        request = CopyImageRequest.CopyImageRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId', self.s_RegionId)
        request.add_query_param('DestinationRegionId', self.d_DestinationRegionId)
        request.add_query_param('DestinationImageName', self.d_DestinationImageName + d_timer)
        request.add_query_param('DestinationDescription', self.d_DestinationDescription + d_timer)
        request.add_query_param('ImageId', imageid)
        response = self.ecshelper.do_action_with_exception(request)
        self.logoper.info('复制镜像任务已提交,镜像id:%s' % json.loads(response)['ImageId'])
        print('复制镜像任务已提交,镜像id:%s' % json.loads(response)['ImageId'])
        return json.loads(response)['ImageId']

    def run(self):
        for instance_id in self._get_Instance():
            s_imageid = self._create_image(instance_id)
            self._copy_image(s_imageid)

if __name__ == '__main__':
    ecsoper = EcsOper(logger)
    ecsoper.run()






