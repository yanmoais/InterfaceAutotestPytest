#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午10:54
from util_tools.logger import Logger
from common.Base_API import Base_Api
from util_tools.Faker import *


class core_zjly_api:
    def __init__(self):
        self.base_api = Base_Api()
        self.now_time = get_time_stand()
        self.logging = Logger().init_logger()

    # 还款申请请求，接收加密数据
    def test_apply_repayment(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送还款申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/applyRepayment", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款状态查询请求，接收加密数据
    def test_apply_repayment_query(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送还款状态查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/applyRepayment_query", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 签约申请请求，接收加密数据
    def test_binding_card_apply(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送签约申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/binding_card_apply", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 签约确认请求，接收加密数据
    def test_binding_card_confirm(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送签约确认请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/binding_card_confirm", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 签约查询请求，接收加密数据
    def test_binding_card_query(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送签约查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/binding_card_query", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款试算请求，接收加密数据
    def test_calculation_repayment_before(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送还款试算请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/calculationRepaymentBefore", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款申请请求，接收加密数据
    def test_loan_apply_settle(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送借款申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/loanApply_settle", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款状态查询请求，接收加密数据
    def test_loan_apply_settle_query(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送借款状态查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/loanApply_settleQuery", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 还款计划查询请求，接收加密数据
    def test_loan_apply_order_query(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送还款计划查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/loanApplyOrder_query", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 借款试算请求，接收加密数据
    def test_calculation_Loan_Before(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送借款试算请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/calculationLoanBefore", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 授信申请请求，接收加密数据
    def test_order_apply(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送授信申请请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/orderApply", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 授信状态查询请求，接收加密数据
    def test_order_apply_query(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送授信状态查询请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/orderApply_query", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 代偿的还款计划同步请求，接收加密数据
    def test_compensatory_plan_update(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'], "appid": encry_requst_data['appid'],
                        "sign": encry_requst_data['sign'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送还款计划同步请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/compensatory_plan_update", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 撞库/用户准入请求，接收加密数据
    def test_zl_zk(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'],
                        "sign": encry_requst_data['sign'],
                        "requestNo": encry_requst_data['requestNo'], "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送撞库/用户准入请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/ZL001", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")

    # 文件上传请求，接收加密数据
    def test_file_upload(self, encry_requst_data):
        request_data = {"timeStamp": encry_requst_data['timeStamp'],
                        "sign": encry_requst_data['sign'],
                        "requestData": encry_requst_data['requestData'],
                        "key": encry_requst_data['key']}
        try:
            self.logging.info(f"开始发送文件上传请求：========，请求数据为{request_data}")
            resp = self.base_api.post("/v1/fileupload", request_data)
            self.logging.info(f"返回结果数据为：=======，{resp}")
            return resp
        except Exception as e:
            self.logging.info(f"请求发生异常，======={e}")


if __name__ == '__main__':
    ss = core_zjly_api().test_compensatory_plan_update()
    print(ss)
