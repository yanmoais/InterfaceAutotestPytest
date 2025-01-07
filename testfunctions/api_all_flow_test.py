#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午10:12
from testcase.test_api_flow.test_ZxRepay_Api_Flow import *
from testcase.test_api_flow.test_XiaoMiLoanRepay_Api_Flow import *
from common.Update_Database_Result import Update_Sql_Result
from common.Core_Risk_API import core_risk_api


# api全流程振兴放款成功
def test_zx_loan_success():
    test_zx_loan_success_api_flow()


# api全流程小米放款成功
def test_xm_loan_success():
    test_xiaomi_loan_success_api_flow()


# api全流程振兴D0批扣还款第一期
def test_zx_d0_repay():
    test_zx_repay_d0_success_api_flow()


# 更新api侧对应渠道为限流模式
def test_api_to_non_funds(channel_code='ICE_ZLSK_36'):
    Update_Sql_Result().update_api_chanel_non_funds(channel_code)


# 更新api侧对应渠道为路由模式
def test_api_to_funds_router(channel_code='ICE_ZLSK_36'):
    Update_Sql_Result().update_api_chanel_funds_router(channel_code)


# 风控白名单加白
def test_risk_phone_pass():
    core_risk_api().test_risk_add_phone("15001060001",
                                        "15001060002",
                                        "15001060003",
                                        "15001060004",
                                        "15001060005",
                                        "15001060006")
