#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03

"""
    request请求方法二次封装，定义基本的环境参数
"""
import logging
import traceback
import requests
import logging
import json
from util_tools.Faker import *
from requests import Response
from config.testconfig import config
from util_tools.logger import Logger
import allure


class Base_Api:
    def __init__(self, ENV=None):
        self.req = requests
        if ENV == 'zfpt':
            self.uri = config['test_zfpt_host']
        else:
            self.uri = config['test_gz_host']
        self.headers = {"Content-Type": "application/json"}
        self.logging = Logger().init_logger()

    def post(self, apis, param_data):
        try:
            response = self.req.post(url=self.uri + apis, json=param_data, headers=self.headers)
            # self.logging.info(f"请求的数据为：======{param_data}")
            return response.json()
        except Exception as e:
            self.logging.error(f"请求接口异常，异常原因{traceback.format_exc(10)}")
            return False, e


if __name__ == '__main__':
    ss = Base_Api()
    print(ss.headers)
