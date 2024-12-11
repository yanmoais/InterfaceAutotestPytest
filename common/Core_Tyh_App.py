"""
    加解密
"""
import json
import logging
from common.Base_API import Base_Api
from util_tools.Faker import *
from util_tools.logger import Logger


class Core_tyh_app(Base_Api):
    def __init__(self):
        super().__init__(ENV="TYH_APP")
        self.base_api = Base_Api(ENV="TYH_APP")
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 发送短信验证码
    def test_sms_send(self, request_data1):
        apis = "/app/app/auth/sms-send"
        try:
            # 需要将数据再次格式化成带转义符并且去除空格
            data = json_dumps_format(request_data1)
            login_data = self.base_api.post("/app/app/auth/sms-send", data)
            self.logging.info(f"返回数据为：======{login_data}")
            authorization = 'Bearer ' + login_data['data']['token']
            self.logging.info(f"返回数据为==========,{login_data}")
            self.logging.info(f"返回数据为==========,{login_data['data']['token']}")
            self.logging.info(f"token为==========,{authorization}")
            assert login_data['msg'] in '操作成功'
        #   return authorization
        except Exception as e:
            self.logging.info(f"发送短信验证码异常=======，异常信息：{e}")
        time.sleep(1)

    # 登录请求
    def test_login_param(self, request_data2):
        apis = "/api/login"
        try:
            # 需要将数据再次格式化成带转义符并且去除空格
            data = json_dumps_format(request_data2)
            login_data = self.base_api.post("/app/app/auth/login", data)
            self.logging.info(f"返回数据为：======{login_data}")
            authorization = 'Bearer ' + login_data['data']['token']
            self.logging.info(f"返回数据为==========,{login_data}")
            self.logging.info(f"返回数据为==========,{login_data['data']['token']}")
            self.logging.info(f"token为==========,{authorization}")
            return authorization
        except Exception as e:
            self.logging.info(f"登录异常=======，异常信息：{e}")
        time.sleep(2)

    #获取商城用户
    def test_quota(self, headers):
        # headers['Authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/home/quota", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['Authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"查询用户额度数据为：======{response_data}")
            return response_data
        except Exception as e:
            self.logging.info(f"查询用户额度异常=======，异常信息：{e}")

    #获取放款账单卡片状态
    def test_loancard_info(self, headers):
        # headers['authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/home/loan-card-info", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"查询放款信息为：======{response_data}")
            return response_data
        except Exception as e:
            self.logging.info(f"查询放款信息=======，异常信息：{e}")

    #获取还款账单卡片状态
    def test_repaycard_info(self, headers):
        # headers['authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/home/repay-card-info", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"查询还款信息为：======{response_data}")
            return response_data
        except Exception as e:
            self.logging.info(f"查询还款信息=======，异常信息：{e}")

    def test_loan_url(self, headers):
        # headers['authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/home/loan-url", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"获取H5借款链接为：======{response_data}")
            return response_data
        except Exception as e:
            self.logging.info(f"获取H5借款链接=======，异常信息：{e}")
    def test_loan_record(self, headers):
        # headers['authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/person-centre/loan-record", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"查询借款记录为：======{response_data}")
            return response_data
        except Exception as e:
            self.logging.info(f"查询借款记录=======，异常信息：{e}")
    def test_repay_list(self, headers):
        headers['authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/person-centre/repay-list", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"查询还款订单列表为：======{response_data}")
            partnerLoanNo = response_data['data']['partnerLoanNo']
            self.logging.info(f"还款订单号为==========,{partnerLoanNo}")
            return response_data
        except Exception as e:
            self.logging.info(f"查询还款订单列表=======，异常信息：{e}")

    def test_repay_url(self, headers):
        # headers['authorization'] = self.test_login_param(request_data2)
        try:
            response_data = self.base_api.get("/app/app/person-centre/repay-list", headers=headers)
            # self.logging.info(f"请求headers为：======{headers['authorization']}")
            self.logging.info(f"请求headers：======{headers}")
            self.logging.info(f"查询借款记录为：======{response_data}")
            return response_data
        except Exception as e:
            self.logging.info(f"查询借款记录=======，异常信息：{e}")
if __name__ == '__main__':

    request_data1 = {'phone': '13812317169',
                     'type': 'login',
                     'ticket': '123456',
                     "nonstr": '123456'
                     }

    request_data2 = {
        'device': '17327587667912371212',
        'captcha': '888888',
        'account': '13812317169',
        'deviceModel': 'PC',
        'loginType': 'ios',
        'osVersion': 'Windows 10 x64'
    }

    # print(register().test_login_param(request_data))
    print(Core_tyh_app().test_sms_send(request_data1))
    print(Core_tyh_app().test_login_param(request_data2))
   # print(Core_tyh_app().test_quota(request_data2))
    print(Core_tyh_app().test_repay_list(request_data2))