#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午3:22
import json

import requests

from util_tools.logger import Logger
from common.Base_API import Base_Api
from util_tools.Faker import *
from common.Encrypt_Decrypt import encrypt_decrypt
from config.testconfig import config

"""
    API全流程接口定义
"""


class core_zfpt_api(Base_Api):
    def __init__(self):
        super().__init__(ENV="zfpt")
        self.base_api = Base_Api(ENV="zfpt")
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 支付平台加密请求数据
    def zfpt_param_encry(self, request_data):
        apis = "/paramsEncryption"
        try:
            # 需要将数据再次格式化成带转义符并且去除空格
            data = json_dumps_format(request_data)
            self.logging.info(f"开始加密请求数据==========,{data}")
            encry_data = self.base_api.post(apis, data)
            return encry_data
        except Exception as e:
            self.logging.info(f"请求数据加密异常=======，异常信息：{e}")

    # 支付平台解密返回数据
    def zfpt_param_decry(self, response_data):
        apis = "/paramsDecryption"
        try:
            self.logging.info(f"开始解密返回数据==========,{response_data}")
            encry_data = self.base_api.post(apis, response_data)
            return encry_data
        except Exception as e:
            self.logging.info(f"返回数据解密异常=======，异常信息：{e}")

    # 支付中台，绑卡签约申请接口，接收加密数据
    def zfzt_bind_bank_apply(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key'],
                        "requestData": encry_requst_data['requestData']}
        try:
            self.logging.info(f"开始发送支付中台绑卡签约申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/bindBankApply", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 支付中台，绑卡签约确认接口，接收加密数据
    def zfzt_bind_bank_confirm(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key'],
                        "requestData": encry_requst_data['requestData']}
        try:
            self.logging.info(f"开始发送支付中台绑卡签约确认请求：========，请求数据为{request_data}")
            print(self.uri)
            resp = self.base_api.post("/v1/bindBankConfirm", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 支付中台，渠道协议号同步接口，接收加密数据
    def zfzt_agrm_no_sync(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key'],
                        "requestData": encry_requst_data['requestData']}
        try:
            self.logging.info(f"开始发送支付中台渠道协议号同步请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/agrmNoSync", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 支付中台，聚合支付申请接口，接收加密数据
    def zfzt_together_withhold_apply(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key'],
                        "requestData": encry_requst_data['requestData']}
        try:
            self.logging.info(f"开始发送支付中台聚合支付申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/togetherWithholdApply", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 支付中台，扣款申请接口，接收加密数据
    def zfzt_withhold_apply(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key'],
                        "requestData": encry_requst_data['requestData']}
        try:
            self.logging.info(f"开始发送支付中台扣款申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/withholdApply", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 支付中台，扣款查询接口，接收加密数据
    def zfzt_withhold_query(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送支付中台扣款查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/withholdQuery", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 支付中台，已绑银行卡查询接口，接收加密数据
    def zfzt_bind_bank_query(self, reqsn, businessChannel, encry_requst_data):
        request_data = {"reqSn": reqsn, "timeStamp": encry_requst_data['timeStamp'],
                        "businessChannel": businessChannel,
                        "sign": encry_requst_data['sign'],
                        "key": encry_requst_data['key'],
                        "requestData": encry_requst_data['requestData']}
        try:
            self.logging.info(f"开始发送支付中台已绑银行卡查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/bindBankQuery", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")


if __name__ == '__main__':
    api = core_zfpt_api()
    print(api.uri)
    # resp = api.test_check_user(data)
    # datas = api.api_param_decry(resp)
    # print(resp)
