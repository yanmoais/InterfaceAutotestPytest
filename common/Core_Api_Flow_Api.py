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


class core_api_flow_api(Base_Api):
    def __init__(self):
        super().__init__(ENV="api")
        self.base_api = Base_Api(ENV="api")
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 客户撞库校验
    def test_check_user(self, encry_request_data):
        try:
            self.logging.info(f"开始发送撞库校验请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/checkUser", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 授信审核结果通知（告知下游更新订单）
    def test_notice_credit_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送授信结果通知请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/noticeCreditResult", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 授信审核结果查询，下游来主动查询结果
    def test_query_credit_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送授信审核结果查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/queryCreditResult", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 授信申请
    def test_apply_credit(self, encry_request_data):
        try:
            resp = self.base_api.api_post("/applyCredit", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款试算
    def test_loan_trial(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款试算请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/loanTrial", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请
    def test_apply_loan(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/applyLoan", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请结果通知（告知下游更新订单）
    def test_notice_loan_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款申请结果通知请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/noticeLoanResult", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请结果查询
    def test_query_loan_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/queryLoanResult", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借据&还款计划查询
    def test_query_loan_plan(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借据&还款计划查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/queryLoanPlan", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 额度&产品查询
    def test_query_credit_product(self, encry_request_data):
        try:
            self.logging.info(f"开始发送额度&产品查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/queryCreditProduct", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 绑卡/请求鉴权/绑卡申请
    def test_apply_certification(self, encry_request_data):
        try:
            self.logging.info(f"开始发送请求鉴权/绑卡申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/applyCertification", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 验证鉴权/发送验证码
    def test_verify_code(self, encry_request_data):
        try:
            self.logging.info(f"开始发送验证鉴权/发送验证码请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/verifyCode", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 查询绑卡列表
    def test_query_card_list(self, encry_request_data):
        try:
            self.logging.info(f"开始发送查询绑卡列表请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/queryCardList", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款试算
    def test_repay_trial(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款试算请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/repayTrial", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款申请
    def test_apply_repayment(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/applyRepayment", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款结果查询
    def test_query_repay_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款结果查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/queryRepayResult", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款结果通知（告知下游还款结果）
    def test_notice_repayment(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款结果通知请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.api_post("/noticeRepayment", json.loads(json_dumps_cn(encry_request_data)))
            self.logging.info(f"返回结果数据为：=======，{json_dumps_cn(resp)}")
            return json_dumps_cn(resp)
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # api加密请求数据
    def api_param_encry(self, data, channel_code="ICE_ZLSK_36"):
        headers = {"Content-Type": "application/json",
                   "channelCode": channel_code}
        apis = "/apiDecrypt/encrypt"
        if channel_code in {"R360", "LXJ", "XL_LY", "RS", "QXL"}:
            self.logging.error(f"{channel_code} 不适用本套接口，请选择合适的渠道！")
            raise ValueError(f"{channel_code} 不适用本套接口，请选择合适的渠道！")
        else:
            try:
                # 需要将数据再次格式化成带转义符并且去除空格
                self.logging.info(f"请求的加密数据：{data}")
                encry_data = requests.post(url=config['test_api_end_host'] + apis, json=data, headers=headers)
                return encry_data.text
            except Exception as e:
                self.logging.info(f"请求数据加密异常=======，异常信息：{e}")

    # api解密请求数据
    def api_param_decry(self, request_data):
        headers = {"Content-Type": "application/json"}
        apis = "/apiDecrypt/decrypt"
        try:
            self.logging.info(f"开始解密请求数据==========,{request_data}")
            decry_data = requests.post(url=config['test_api_end_host'] + apis, data=request_data, headers=headers)
            self.logging.info(f"返回解密数据为==========,{decry_data.json()}")
            return decry_data.json()
        except Exception as e:
            self.logging.info(f"请求数据解密异常=======，异常信息：{e}")


if __name__ == '__main__':
    phone = '15915370864'
    id_card = '360724199402101018'
    api = core_api_flow_api()
    data = api.api_param_encry("DSD", "RS")
    print(data)
    # resp = api.test_check_user(data)
    # datas = api.api_param_decry(resp)
    # print(resp)
