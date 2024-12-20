#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午5:34
import json
import requests
from util_tools.logger import Logger
from common.Base_API import Base_Api
from util_tools.Faker import *
from common.Encrypt_Decrypt import encrypt_decrypt
from config.testconfig import config
from util_tools.Read_Yaml import read_risk_phone


class core_risk_api(Base_Api):
    def __init__(self):
        super().__init__(ENV="RISK")
        self.base_api = Base_Api(ENV="RISK")
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 风控手机号白名单加白
    def test_risk_add_phone(self, encry_request_data):
        try:
            data = {
                "data": [
                    encry_request_data
                ]
            }
            self.logging.info(f"开始发送风控加白请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/drms/risk_management/white/add",
                                          json_dumps_cn(data))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")


if __name__ == '__main__':
    api = core_risk_api()
    print(api.uri)
    phone = read_risk_phone()
    data = {
        "data": [
            "15915370822"
        ]
    }
    resp = api.test_risk_add_phone(data)
    print(resp)
