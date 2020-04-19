import re
from configparser import ConfigParser

import requests

from porttest import logger


class check_ports():
    def __init__(self, logger):
        """
            初始化，获取配置文件信息
        """
        self.url = 'http://tool.chinaz.com/iframe.ashx?t=port'
        self.headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '62',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'tool.chinaz.com',
            'Origin': 'http://tool.chinaz.com',
            'Referer': 'http://tool.chinaz.com/port/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        config = ConfigParser()
        config.read('info.cfg', encoding='utf-8')
        self.address_list = config['port_check_info']['address']
        self.port_list = config['port_check_info']['ports']
        # 初始化logger
        logger = logger.LogHelper()
        logname = logger.create_dir()
        self.logoper = logger.create_logger(logname)

    # def _get_body(self):
    #     """
    #     获取address和port
    #     :return: list
    #     """
    #     address_list = self.address_list.split(',')
    #     port_list = self.port_list.split(',')
    #
    #     # 处理端口范围，返回range
    #     range_flag = False
    #     port_range = None
    #     content_List_range = []
    #     for port in port_list:
    #         if '-' in port:
    #             range_flag = True
    #             port_range = range(int(port.split('-')[0]),int(port.split('-')[1])+1)
    #             port_list.remove(port)
    #
    #     # 处理总体list
    #     for add in address_list:
    #         if range_flag:
    #             for port in port_range:
    #                 content_List_range.append(add + ':' + str(port))
    #
    #     # 合并range和普通list
    #     content_List = [ add+':'+port for add in address_list for port in port_list ]
    #     content_List_range.extend(content_List)
    #     return content_List_range
    def _get_body(self):
        """
        获取address和port
        :return:list
        """
        address_list = self.address_list.split(",")
        port_list = self.port_list.split(',')

        # 处理端口范围,返回range
        range_flag = False
        port_range = None
        content_List_range = []
        for port in port_list:
            if '-' in port:
                range_flag = True
                port_range = range(int(port.split('-')[0]), int(port.split('-')[1]) + 1)
                port_list.remove(port)

        # 处理总体list
        for add in address_list:
            if range_flag:
                for port in port_range:
                    content_List_range.append(add + ':' + str(port))

        # 合并range和普通list
        content_List = [add + ':' + port for add in address_list for port in port_list]
        content_List_range.extend(content_List)
        return content_List_range


    def run(self):
        """
            进行端口检测
            :return:
            """
        for content in self._get_body():
            content_list = content.split(':')
            body = {
                'host': content_list[0],
                'port': content_list[1],
                'encode': 'tlCHS1u3IgF4sC57m6KOP3Oaj1Y1kfLq'
            }

            try:
                response = requests.post(url=self.url, data=body, headers=self.headers)
                print(response.text)
                port_status = re.findall("msg:'(.*?)'", response.text)
                if len(port_status) > 0:
                    print('%s,port status is:%s' % (content, port_status))
                    self.logoper.info('%s,port status is:%s' % (content, port_status))
                else:
                    self.logoper.info('%s,port status is:%s' % (content, port_status))
                    print('Occer error！请输入正确的地址和端口')
            except Exception as e:
                self.logoper.info(e)


if __name__ == '__main__':
    check_app = check_ports(logger)
    check_app.run()
