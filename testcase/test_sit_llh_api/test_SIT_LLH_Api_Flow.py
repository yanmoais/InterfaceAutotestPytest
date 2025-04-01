#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:10
import requests
import time
import pytest
import allure
from common.Encrypt_Decrypt import encrypt_decrypt
from config.testconfig import channel_codes
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Tyh_Api import core_tyh_api
from util_tools.Read_photo import *
from util_tools.Read_Yaml import read_risk_phone
from common.Update_Database_Result import Update_Sql_Result
from common.Update_Database_Result import Update_Sql_Result
from util_tools.Xxl_Job_Executor import execute_xxl_job
from common.Select_Database_Result import Select_Sql_Result
from util_tools.Loop_Result_Tyh import loop_result_tyh

# 初始化环境参数
host = "http://gzdev.ffyla.com:26801"
headers = {"Content-Type": "application/json;charset=UTF-8"}
channelId = "LLH_XY"


# 借款链接H5
def test_sit_llh_yx_credit_h5_success():
    with allure.step("数据初始化"):
        # 初始化环境参数
        host = "http://gzdev.ffyla.com:26801"
        headers = {"Content-Type": "application/json"}
        channelId = "LLH_XY"
        public_param = {
            "partner": channelId
        }
        enc = encrypt_decrypt()
        credit_apply_no = get_credit_apply_no("LLH_")
        db = Update_Sql_Result()
        apply_time = get_time_stand_api()
        id_no, birthday = get_zx_user_id_no(year_s=1990, year_e=2019)
        user_name = get_user_name()
        user_id = get_cust_id()
        bank_card_no = get_baofu_ccb_num()
        certificationApplyNo = get_api_bk_id()
        logging = Logger().init_logger()

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：金美信  ==  JMX
        loanApplyNo = get_req_seq_no("JMX")
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = "LLH_XY"
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "LLH"

    with allure.step("用户撞库"):
        # 撞库数据,以手机号为主
        public_param["data"] = {"md5": enc.param_encry_by_md5(mobile_no), "mode": "M"}
        print(public_param)
        # 发送撞库请求
        zk_resp = requests.post(url=host + "/checkUser", json=public_param, headers=headers)
        # 撞库解密
        logging.info(f"撞库返回结果为：======{zk_resp.text}")

    with allure.step("授信审核申请"):
        # 授信申请数据
        sx_need_encry_data = {"userId": user_id, "creditApplyNo": credit_apply_no, "applyTime": apply_time,
                              "productCode": product_code, "applyAmount": "20000.00",
                              "userInfo": {"mobile": mobile_no, "name": user_name, "idCardNo": id_no, "marriage": "20",
                                           "monthlyIncome": "4", "education": "20", "job": "1", "province": "广东省",
                                           "city": "广州市", "district": "番禺区",
                                           "addrDetail": "广东省广州市番禺区成钧街道豪承小区190号楼501"},
                              "idCardOcrInfo": {"positive": get_positive_photo(), "negative": get_negative_photo(),
                                                "nameOCR": user_name, "idCardNoOCR": id_no, "beginTimeOCR": "20230829",
                                                "duetimeOCR": "20991231",
                                                "addressOCR": "广东省广州市番禺区成钧街道豪承小区190号楼501",
                                                "sexOCR": "M", "ethnicOCR": "汉族", "issueOrgOCR": "广州市公安局"},
                              "faceInfo": {"assayTime": apply_time, "assayType": "SENSETIME", "best": get_best_photo()},
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455377",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209187"},
                              "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                               "userName": user_name, "bankCardNo": bank_card_no},
                              "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"},
                              "companyInfo": {
                                  "companyName": "中国建筑集团有限公司",
                                  "province": "440000",
                                  "city": "440100", "district": "440114",
                                  "companyAddr": "广东省广州市番禺区三里河路15号"},
                              "agreementTime": apply_time,
                              "extendInfo": {
                                  "UTag": "C",
                                  "mobileMode": "21091116AC",
                                  "networkType": "",
                                  "system": "android",
                                  "systemVersion": "13"}}
        public_param["data"] = sx_need_encry_data
        print(public_param)
        # 发送授信请求
        sx_resp = requests.post(url=host + "/applyCredit", json=public_param, headers=headers)
        # 授信返回结果
        logging.info(f"授信返回结果为：======{sx_resp.text}")

    # with allure.step("授信结果查询"):
    #     partnerCreditNo = ""
    #     # 授信结果查询数据
    #     sx_result_data = {"userId": user_id, "partnerCreditNo": partnerCreditNo}
    #     public_param["data"] = sx_result_data
    #     # 发送授信结果查询请求
    #     sx_result_resp = requests.post(url=host + "/queryCreditResultByPartner", json=sx_result_data, headers=headers)
    #     # 授信结果返回数据
    #     logging.info(f"授信结果返回结果为：======{sx_result_resp.json()}")
    #
    # with allure.step("获取H5借款链接"):
    #     # 借款链接请求数据
    #     loan_h5_data = {"userId": user_id,
    #                     "partnerCreditNo": partnerCreditNo,
    #                     "loanApplyNo": loanApplyNo,
    #                     "pageType": "1"}
    #     public_param["data"] = loan_h5_data
    #     # 发送借款链接H5请求
    #     loan_h5_resp = requests.post(url=host + "/outsideLink", json=public_param, headers=headers)
    #     # 借款链接
    #     logging.info(f"借款链接:{loan_h5_resp.json()}")


# 还款链接H5
def test_sit_llh_yx_repay_h5_success():
    with allure.step("数据初始化"):
        # 初始化环境参数
        host = "http://gzdev.ffyla.com:26801"
        headers = {"Content-Type": "application/json"}
        channelId = "LLH_XY"
        public_param = {
            "partner": channelId
        }

        logging = Logger().init_logger()

    # 修改对应的数据
    repayApplyNo = get_repay_no()
    partnerCreditNo = ""
    user_id = ""
    partnerLoanNo = ""
    loanApplyNo = ""

    with allure.step("获取H5借款链接"):
        # 借款链接请求数据
        loan_h5_data = {"userId": user_id,
                        "partnerCreditNo": partnerCreditNo,
                        "partnerLoanNo": partnerLoanNo,
                        "loanApplyNo": loanApplyNo,
                        "repayApplyNo": repayApplyNo,
                        "pageType": "2"}
        public_param["data"] = loan_h5_data
        # 发送借款链接H5请求
        loan_h5_resp = requests.post(url=host + "/outsideLink", json=public_param, headers=headers)
        # 借款链接
        logging.info(f"借款链接:{loan_h5_resp.json()}")
