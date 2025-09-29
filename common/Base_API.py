#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03

"""
    request请求方法二次封装，定义基本的环境参数
"""
import traceback
import requests
from util_tools.Faker import *
from requests import Response
from config.testconfig import config
from util_tools.logger import Logger


class Base_Api:
    def __init__(self, ENV=None):
        self.req = requests
        if ENV == 'zfpt':
            self.uri = config['test_zfpt_host']
        elif ENV == 'app':
            self.uri = config['test_app_host']
            self.headers = {"Content-Type": "application/json"}
        elif ENV == 'api':
            self.uri = config['test_api_host']
        elif ENV == 'RISK':
            self.uri = config['risk_host']
        elif ENV == "TYH_HY":
            self.uri = config['test_tyh_hy_host']
        elif ENV == "TYH_APP":
            self.uri = config['test_tyh_app_host']
        else:
            self.uri = config['test_zjly_host']

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

    def get(self, apis, headers):
        try:
            response = self.req.get(url=self.uri + apis, headers=headers)
            # self.logging.info(f"请求的数据为：======{param_data}")
            return response.json()
        except Exception as e:
            self.logging.error(f"请求接口异常，异常原因{traceback.format_exc(10)}")
            return False, e

    def api_post(self, apis, param_data):
        try:
            response = self.req.post(url=self.uri + apis, data=param_data, headers=self.headers)
            # self.logging.info(f"请求的数据为：======{param_data}")
            return response.json()
        except Exception as e:
            self.logging.error(f"请求接口异常，异常原因{traceback.format_exc(10)}")
            return False, e

    def app_post(self, apis, param_data, headers):
        try:
            response = self.req.post(url=self.uri + apis, json=param_data, headers=self.headers)
            # self.logging.info(f"请求的数据为：======{param_data}")
            return response.json()
        except Exception as e:
            self.logging.error(f"请求接口异常，异常原因{traceback.format_exc(10)}")
            return False, e

    def post_dingk(self, uri, param_data, headers):
        try:
            response = self.req.post(url=uri, json=param_data, headers=headers)
            return response.json()
        except Exception as e:
            self.logging.error(f"请求接口异常，异常原因{traceback.format_exc(10)}")
            return False, e


if __name__ == '__main__':
    ss = Base_Api()
    print(ss.uri)
