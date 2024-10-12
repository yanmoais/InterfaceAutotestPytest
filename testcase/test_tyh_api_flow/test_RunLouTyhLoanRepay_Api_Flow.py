#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:20

import time
import pytest
import allure
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Tyh_Api import core_tyh_api
from util_tools.Read_photo import *
from util_tools.Read_Yaml import read_risk_phone
from common.Update_Database_Result import Update_Sql_Result
from util_tools.Loop_result import loop_result
from util_tools.Xxl_Job_Executor import execute_xxl_job


@pytest.mark.run(order=10)
@allure.epic("天源花渠道-润楼资方-天源花API全流程")
@allure.feature("天源花渠道-授信模块-天源花API全流程")
@allure.title("天源花渠道-借款成功-天源花API全流程")
@allure.story("天源花渠道-润楼资方授信案例-天源花API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_tyh_runlou_loan_success():
    with allure.step("数据初始化"):
        api = core_tyh_api()
        credit_apply_no = get_credit_apply_no()
        db = Update_Sql_Result()
        apply_time = get_time_stand_api()
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        bank_card_no = get_baofu_ccb_num()
        certificationApplyNo = get_api_bk_id()
        logging = Logger().init_logger()

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：润楼  ==  RL
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "FR_RUN_LOU"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = "TYH_HY"
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "TYH_HY"

        # 借款申请单号
        loanApplyNo = "7b83fa01bfe54cfd813461ff103bea35"
        # 用户ID
        user_id = "3fc03cd7-ec66-41c0-8a0e-189378a70afe"

    with allure.step("借款结果查询"):
        # 借款查询数据
        loan_query_need_encry_data = {
            "userId": user_id,
            "loanApplyNo": loanApplyNo
        }
        # 加密借款查询数据
        encry_data = api.api_param_encry(loan_query_need_encry_data)
        # 发送查询借款结果
        loan_query_resp = api.test_query_loan_result(encry_data)
        # 解密借款查询结果
        loan_query_resp = api.api_param_decry(loan_query_resp)
        logging.info(f"借款查询结果解密为：==== {loan_query_resp}")


@pytest.mark.run(order=11)
@allure.epic("天源花渠道-润楼资方-天源花API全流程")
@allure.feature("天源花渠道-授信模块-天源花API全流程")
@allure.title("天源花渠道-借款成功-天源花API全流程")
@allure.story("天源花渠道-润楼资方授信案例-天源花API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_tyh_runlou_repay_success():
    with allure.step("数据初始化"):
        api = core_tyh_api()
        credit_apply_no = get_credit_apply_no()
        db = Update_Sql_Result()
        apply_time = get_time_stand_api()
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        bank_card_no = get_baofu_ccb_num()
        certificationApplyNo = get_api_bk_id()
        logging = Logger().init_logger()

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：润楼  ==  RL
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "FR_RUN_LOU"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = "TYH_HY"
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "TYH_HY"

        # 借款申请单号
        loanApplyNo = "7b83fa01bfe54cfd813461ff103bea35"
        # 用户ID
        user_id = "3fc03cd7-ec66-41c0-8a0e-189378a70afe"
        # 还款申请单号
        repayApplyNo = "014012d29cc24ee98452ed59256910cb"

    with allure.step("还款结果查询"):
        # 还款结果查询数据
        loan_query_need_encry_data = {
            "userId": user_id,
            "repayApplyNo": repayApplyNo
        }
        # 还款结果查询数据
        encry_data = api.api_param_encry(loan_query_need_encry_data)
        # 发送查询还款结果
        repay_query_resp = api.test_query_repay_result(encry_data)
        # 解密还款结果查询
        repay_query_resp = api.api_param_decry(repay_query_resp)
        logging.info(f"还款结果解密为：==== {repay_query_resp}")
