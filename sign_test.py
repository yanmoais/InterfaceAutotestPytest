#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:28
import time
import pytest
import allure
from conftest import get_channel
from common.Select_Database_Result import Select_Sql_Result
from config.testconfig import channel_codes
from testdata.assert_data.banding_assert_data import *
from testdata.assert_data.loan_assert_data import *
from testdata.assert_data.loan_credit_amt_assert_data import credit_amt_query_success_data
from util_tools.Public_Assert import loan_success_assert, banding_card_success_assert, loan_credit_amt_success_assert
from util_tools.Xxl_Job_Executor import execute_xxl_job
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Api_Flow_Api import core_api_flow_api
from common.Encrypt_Decrypt import encrypt_decrypt
from util_tools.Read_photo import *
from util_tools.Read_Yaml import read_risk_phone
from common.Update_Database_Result import Update_Sql_Result
from util_tools.Loop_result import loop_result
import requests


def test_sign_contract_performance():
    apply_no = get_contract_no()
    biz_no = get_req_no()
    # 核心api的基类
    api = core_api_flow_api()
    request_data = {
        "signApplyNo": apply_no,
        "custNo": "CT1940393672494444544",
        "bizNo": biz_no,
        "bizType": "credit",
        "requestCode": "equtity_platform",
        "signRoleList": [
            {
                "signRoleType": "1",
                "signRoleCode": "36"
            },
            {
                "signRoleType": "1",
                "signRoleCode": "59"
            }
        ],
        "contractNodeType": "302",
        "params": json_dumps_cn(
            {"userName": "攒钱花", "userIdCardNo": "450126198611145516", "userMobile": "15500000007",
             "sysYear": "2025", "sysMonth": "3", "sysDay": "20"})
    }
    header = {
        "content-type": "application/json"
    }
    # 加密数据
    encry_request_data = api.api_param_encry(request_data, "RP")
    payload = encry_request_data
    print(f"加密后的数据为：{request_data}")
    # 发送请求
    reps = requests.request("POST", url=f"http://ags-platform-sit.zhonglishuke.com/contract/sign", json=payload,
                            headers=header)
    # reps = self.client.post(url=f"http://ags-platform-sit.zhonglishuke.com/contract/sign", json=payload,
    #                         headers=header)
    # 解密
    print(f"请求返回的结果为：{reps.text}")
    rep = api.api_param_decry(reps)
    print(rep)
