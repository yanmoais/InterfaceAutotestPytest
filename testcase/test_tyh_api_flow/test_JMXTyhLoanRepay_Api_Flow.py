#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:20

import time
import pytest
import allure
from common.Encrypt_Decrypt import encrypt_decrypt
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


@pytest.mark.run(order=10)
@allure.epic("天源花渠道-金美信资方-天源花API全流程")
@allure.feature("天源花渠道-授信模块-天源花API全流程")
@allure.title("天源花渠道-借款成功-天源花API全流程")
@allure.story("天源花渠道-金美信资方授信案例-天源花API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_tyh_jmx_loan_success():
    with allure.step("数据初始化"):
        api = core_tyh_api()
        enc = encrypt_decrypt()
        credit_apply_no = get_credit_apply_no("TYH_")
        db = Update_Sql_Result()
        apply_time = get_time_stand_api()
        id_no, birthday = get_zx_user_id_no(1990, 1998)
        user_name = get_user_name()
        user_id = get_cust_id()
        bank_card_no = get_baofu_ccb_num(('0', '2', '4', '6'))
        certificationApplyNo = get_api_bk_id()
        logging = Logger().init_logger()

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：金美信  ==  JMX
        loanApplyNo = get_req_seq_no("JMX")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "JMX"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = "TYH_HY"
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "TYH_HY"

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds("TYH_HY")

    with allure.step("用户撞库"):
        # 撞库数据,以手机号为主
        zk_need_encry_data = {"md5": enc.param_encry_by_md5(mobile_no), "mode": "M"}
        # 加密撞库数据
        zk_encry_data = api.api_param_encry(zk_need_encry_data, channel_code)
        # 发送撞库请求
        zk_resp = api.test_check_user(zk_encry_data)
        # 撞库解密
        zk_decry_resp = api.api_param_decry(zk_resp)
        logging.info(f"解密后的撞库返回结果为：======{zk_decry_resp}")

    with allure.step("授信审核申请"):
        # 授信申请数据
        sx_need_encry_data = {"userId": user_id, "creditApplyNo": credit_apply_no, "applyTime": apply_time,
                              "productCode": product_code, "applyAmount": "20000.00",
                              "userInfo": {"mobile": mobile_no, "name": user_name, "idCardNo": id_no, "marriage": "20",
                                           "monthlyIncome": "4", "education": "20", "job": "1", "province": "230000",
                                           "city": "230100", "district": "230109",
                                           "addrDetail": "黑龙江省哈尔滨市松北区成钧街道豪承小区190号楼501"},
                              "idCardOcrInfo": {"positive": get_positive_photo(), "negative": get_negative_photo(),
                                                "nameOCR": user_name, "idCardNoOCR": id_no, "beginTimeOCR": "20230829",
                                                "duetimeOCR": "99991231",
                                                "addressOCR": "黑龙江省哈尔滨市松北区成钧街道豪承小区190号楼501",
                                                "sexOCR": "M", "ethnicOCR": "汉族", "issueOrgOCR": "黑龙江公安局"},
                              "faceInfo": {"assayTime": apply_time, "assayType": "SENSETIME", "best": get_best_photo()},
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455377",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209187"},
                              "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                               "userName": user_name, "bankCardNo": bank_card_no},
                              "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"},
                              "companyInfo": {
                                  "companyName": "中国建筑集团有限公司",
                                  "province": "110000",
                                  "city": "110100",
                                  "district": "110108",
                                  "companyAddr": "北京市海淀区三里河路15号"},
                              "agreementTime": apply_time,
                              "extendInfo": {
                                  "UTag": "C",
                                  "mobileMode": "21091116AC",
                                  "networkType": "",
                                  "system": "android",
                                  "systemVersion": "13"}}

        logging.info(f"{json_dumps_cn(sx_need_encry_data)}")
        # 加密授信数据
        sx_encry_data = api.api_param_encry(sx_need_encry_data, channel_code)
        # 发送授信申请请求
        sx_resp = api.test_apply_credit(sx_encry_data)
        # 授信结果解密
        sx_decry_data = api.api_param_decry(sx_resp)
        time.sleep(5)
        partner_creditNo = sx_decry_data["partnerCreditNo"]
        credit_apply_no_tyh = Select_Sql_Result().select_credit_apply_no_by_tyh(credit_apply_no)
        api_user_id = Select_Sql_Result().select_user_id_by_tyh(credit_apply_no_tyh)
        logging.info(f"解密后的授信申请返回结果为：======{sx_decry_data}")

    with allure.step("更新授信相关表为金美信资方"):
        db.update_api_flow_all_table(funds_code, user_id, "tyh")
        db.update_api_flow_all_table(funds_code, api_user_id, "api")
        logging.info(f"数据库更新资方完毕")

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "partnerCreditNo": partner_creditNo}
        # 发起授信结果轮询请求
        resp = loop_result_tyh().loop_tyh_sx_result(sx_cx_data, credit_apply_no)
        logging.info(f"当前授信结果返回数据为：{resp}")

    with allure.step("绑卡申请"):
        # 请求鉴权数据
        bk_jq_need_encry_data = {"userId": user_id, "certificationApplyNo": certificationApplyNo, "bankCode": "0004",
                                 "idCardNo": id_no, "userMobile": mobile_no, "userName": user_name,
                                 "bankCardNo": bank_card_no, "registerMobile": mobile_no, "agreementTime": apply_time
                                 }
        # 判断是360就直接绑卡，不指定bindType
        # 绑卡轮询，并且绑卡两次
        # 此处需要优化，360的话不需要指定bindType,直接绑两次卡就好
        with allure.step("第一次绑卡"):
            if channel_code == "APPZY":
                bk_jq_need_encry_data["bindType"] = "fundsChannel"
            else:
                pass
            loop_result_tyh().loop_tyh_bk_result(bk_jq_need_encry_data, channel_code)
        with allure.step("第二次绑卡"):
            if channel_code == "APPZY" or channel_code == "XL":
                bk_jq_need_encry_data["bindType"] = "payChannel"
            else:
                pass
            # 第二次绑卡需要更新申请号以及时间，从新赋值
            time.sleep(2)
            bk_jq_need_encry_data["certificationApplyNo"], bk_jq_need_encry_data[
                "agreementTime"] = get_api_bk_id(), get_time_stand_api()
            loop_result_tyh().loop_tyh_bk_result(bk_jq_need_encry_data, channel_code)

    with allure.step("借款试算"):
        # 借款试算数据
        jk_ss_need_encry_data = {"userId": user_id, "loanApplyNo": loanApplyNo, "loanTime": apply_time,
                                 "partnerCreditNo": partner_creditNo, "productCode": product_code, "loanAmt": loan_amt,
                                 "loanPurpose": "05", "term": reqPeriods, "repayMethod": "01", "needEquityTrial": "Y",
                                 "agreementTime": apply_time,
                                 "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no}, }
        # 加密借款试算数据
        jk_ss_encry_data = api.api_param_encry(jk_ss_need_encry_data, channel_code)
        # 发起借款试算请求
        jk_ss_resp = api.test_loan_trial(jk_ss_encry_data)
        # 解密试算返回结果
        jk_ss_decry_data = api.api_param_decry(jk_ss_resp)
        logging.info(f"借款试算返回数据结果为：======={jk_ss_decry_data}")

    with allure.step("组装权益信息"):
        eqCode = jk_ss_decry_data['equityTrialDTO']['eqCode']
        cacheEqCode = jk_ss_decry_data['equityTrialDTO']['cacheEqCode']

    with allure.step("借款申请"):
        # 借款申请数据
        jk_sq_need_encry_data = {"loanTime": apply_time, "productCode": product_code, "repayMethod": "01",
                                 "loanPurpose": "05", "partnerCreditNo": partner_creditNo, "term": reqPeriods,
                                 "loanAmt": loan_amt, "loanApplyNo": loanApplyNo, "userId": user_id,
                                 "agreementTime": apply_time,
                                 "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no},
                                 "eqCode": eqCode, "cacheEqCode": cacheEqCode}
        # 加密借款申请数据
        jk_sq_encry_data = api.api_param_encry(jk_sq_need_encry_data, channel_code)
        # 发起借款申请请求
        jk_sq_resp = api.test_apply_loan(jk_sq_encry_data)
        # 解密借款申请返回结果
        jk_sq_decry_data = api.api_param_decry(jk_sq_resp)
        logging.info(f"借款返回数据结果为：======={jk_sq_decry_data}")

    with allure.step("轮询执行JOB借款成功"):
        # 借款查询数据
        loan_query_need_encry_data = {
            "userId": user_id,
            "loanApplyNo": loanApplyNo
        }
        # 发起轮询，并且执行借款过程中需要的JOB
        jk_success_resp = loop_result_tyh().loop_tyh_jk_result(loan_query_need_encry_data, loanApplyNo)
        logging.info(f"借款返回的查询参数是：{jk_success_resp}")

    with allure.step("展示权益信息"):
        # 开通权益数据
        qy_need_encry_data = {"eqCode": eqCode}
        # 加密数据
        qy_encry_data = api.api_param_encry(qy_need_encry_data)
        # 发起权益开通请求
        qy_resp = api.test_query_equity_detail(qy_encry_data)
        # 解密请求结果
        qy_decry_data = api.api_param_decry(qy_resp)
        logging.info(f"权益展示的结果是：{qy_decry_data}")

    with allure.step("天源花人脸跳过"):
        pass

    with allure.step("获取H5链接"):
        loan_h5, repay_h5 = tyh_h5_loan_repay(credit_apply_no, user_id, loanApplyNo)
        logging.info(f"借据信息&还款页面链接为：{loan_h5}{repay_h5}")


@pytest.mark.run(order=11)
@allure.epic("天源花渠道-金美信资方-天源花API全流程")
@allure.feature("天源花渠道-授信模块-天源花API全流程")
@allure.title("天源花渠道-借款成功-天源花API全流程")
@allure.story("天源花渠道-金美信资方授信案例-天源花API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_tyh_jmx_repay_success():
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
        # 修改对应的缩写或其他标志：金美信  ==  JMX
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "JMX"
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
