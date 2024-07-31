#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午3:22
from util_tools.logger import Logger
from common.Base_API import Base_Api
from util_tools.Faker import *
from common.Encrypt_Decrypt import encrypt_decrypt

"""
    API全流程接口定义
"""


class core_api_flow_api(Base_Api):
    def __init__(self):
        super().__init__(ENV="api")
        self.base_api = Base_Api()
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 客户撞库校验
    def test_check_user(self, encry_request_data):
        request_data = {
            "requestNo": encry_request_data['requestNo'], "requestTime": encry_request_data['requestTime'], "partner": "ICE_001",
            "version": "1.0.5",
            "input": encry_request_data['input']
        }
        try:
            self.logging.info(f"开始发送撞库校验请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/checkUser", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 审核结果通知（告知资方更新订单）
    def test_notice_credit_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送审核结果通知请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/noticeCreditResult", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 审核结果查询
    def test_query_credit_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送审核结果查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/queryCreditResult", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款试算
    def test_loan_trial(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款试算请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/loanTrial", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请
    def test_apply_loan(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/applyLoan", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请结果通知（告知资方更新订单）
    def test_notice_loan_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款申请结果通知请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/noticeLoanResult", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请结果查询
    def test_query_loan_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借款申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/queryLoanResult", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借据&还款计划查询
    def test_query_loan_plan(self, encry_request_data):
        try:
            self.logging.info(f"开始发送借据&还款计划查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/queryLoanPlan", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 额度&产品查询
    def test_query_credit_product(self, encry_request_data):
        try:
            self.logging.info(f"开始发送额度&产品查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/queryCreditProduct", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 绑卡/请求鉴权/绑卡申请
    def test_apply_certification(self, encry_request_data):
        try:
            self.logging.info(f"开始发送请求鉴权/绑卡申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/applyCertification", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 验证鉴权/发送验证码
    def test_verify_code(self, encry_request_data):
        try:
            self.logging.info(f"开始发送验证鉴权/发送验证码请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/verifyCode", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 查询绑卡列表
    def test_query_card_list(self, encry_request_data):
        try:
            self.logging.info(f"开始发送查询绑卡列表请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/queryCardList", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款试算
    def test_repay_trial(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款试算请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/repayTrial", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款申请
    def test_apply_repayment(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款申请请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/applyRepayment", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款结果查询
    def test_query_repay_result(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款结果查询请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/queryRepayResult", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款结果通知（告知资方还款结果）
    def test_notice_repayment(self, encry_request_data):
        try:
            self.logging.info(f"开始发送还款结果通知请求：========，请求数据为{encry_request_data}")
            resp = self.base_api.post("/noticeRepayment", encry_request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")


if __name__ == '__main__':
    phone = '15915370864'
    id_card = '360724199402101018'
    enc = encrypt_decrypt()

    data = {"md5": enc.param_encry_by_md5(phone), "mode": "M"}
    print(enc.uri)
    api = core_api_flow_api()
    print(api.uri)
    # resp = api.test_check_user(data)
    # print(data)
    # print(resp)
