#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  上午11:49


import time
import pytest
import allure
from conftest import get_channel
from common.Select_Database_Result import Select_Sql_Result
from config.testconfig import channel_codes
from testdata.assert_data.banding_assert_data import *
from testdata.assert_data.loan_assert_data import *
from testdata.assert_data.loan_credit_amt_assert_data import credit_amt_query_success_data
from util_tools.Loop_result import loop_result
from util_tools.Public_Assert import loan_success_assert, banding_card_success_assert, loan_credit_amt_success_assert
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Api_Flow_Api import core_api_flow_api
from common.Encrypt_Decrypt import encrypt_decrypt
from util_tools.Read_photo import *
from util_tools.Read_Yaml import read_risk_phone
from common.Update_Database_Result import Update_Sql_Result
from util_tools.Loop_result import loop_result
from util_tools.Xxl_Job_Executor import execute_xxl_job


# API全流程-哈密众邦放款成功
@pytest.mark.run(order=10)
@allure.epic("360沙盒渠道-哈密众邦资方-API全流程")
@allure.feature("360沙盒渠道-授信模块-API全流程")
@allure.title("360沙盒渠道-借款成功-API全流程")
@allure.story("360沙盒渠道-哈密众邦资方授信案例-API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_zb_loan_success_api_flow(get_channel):
    with allure.step("数据初始化"):
        api = core_api_flow_api()
        enc = encrypt_decrypt()
        credit_apply_no = get_credit_apply_no()
        db = Update_Sql_Result()
        apply_time = get_time_stand_api()
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        bank_card_no = get_baofu_ccb_num()
        user_id = get_cust_id()
        certificationApplyNo = get_api_bk_id()
        logging = Logger().init_logger()

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：哈密众邦  ==  ZB
        loanApplyNo = get_req_seq_no("ZB")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "HAMI_ZHONGBANG"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = get_channel
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "KN_HALF"

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds(get_channel)
        logging.info(f"开始执行测试方法中渠道 {channel_code} 的测试")

    with allure.step("用户撞库"):
        # 撞库数据,以手机号为主
        zk_need_encry_data = {"params": {"md5": enc.param_encry_by_md5(mobile_no), "mode": "M"}}
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
                              "agreementTime": apply_time}
        logging.info(f"{json_dumps_cn(sx_need_encry_data)}")
        # 加密授信数据
        sx_encry_data = api.api_param_encry(sx_need_encry_data, channel_code)
        # 发送授信申请请求
        sx_resp = api.test_apply_credit(sx_encry_data)
        # 授信结果解密
        sx_decry_data = api.api_param_decry(sx_resp)
        partner_creditNo = sx_decry_data["partnerCreditNo"]
        logging.info(f"解密后的授信申请返回结果为：======{sx_decry_data}")

    with allure.step("更新授信相关表为哈密众邦资方"):
        db.update_api_flow_all_table(funds_code, user_id)
        logging.info(f"数据库更新资方完毕")
        time.sleep(5)

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "creditApplyNo": credit_apply_no}
        # 发起授信结果轮询请求
        resp = loop_result().loop_api_flow_sx_result(sx_cx_data, credit_apply_no, channel_code)
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
            if channel_code in channel_codes:
                bk_jq_need_encry_data["bindType"] = "fundsChannel"
            else:
                pass
            loop_result().loop_api_flow_bk_result(bk_jq_need_encry_data, channel_code)
        with allure.step("第二次绑卡"):
            if channel_code in channel_codes:
                bk_jq_need_encry_data["bindType"] = "payChannel"
            else:
                pass
            # 第二次绑卡需要更新申请号以及时间，从新赋值
            time.sleep(2)
            bk_jq_need_encry_data["certificationApplyNo"], bk_jq_need_encry_data[
                "agreementTime"] = get_api_bk_id(), get_time_stand_api()
            loop_result().loop_api_flow_bk_result(bk_jq_need_encry_data, channel_code)

    with allure.step("借款试算"):
        # 借款试算数据
        # 加密借款试算数据
        # 发起借款试算请求
        # 解密试算返回结果
        pass

    with allure.step("推送客户中心"):
        execute_xxl_job().push_credit_info_to_customer_center(credit_apply_no)
        time.sleep(5)

    with allure.step("借款申请"):
        # 借款申请数据
        jk_sq_need_encry_data = {"loanTime": apply_time, "productCode": product_code, "repayMethod": "01",
                                 "loanPurpose": "05", "partnerCreditNo": partner_creditNo, "term": reqPeriods,
                                 "loanAmt": loan_amt, "loanApplyNo": loanApplyNo, "userId": user_id,
                                 "agreementTime": apply_time,
                                 "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no},
                                 "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455377",
                                                 "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209187"},
                                 "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"}}
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
        jk_success_resp = loop_result().loop_api_flow_loan_result(loan_query_need_encry_data, loanApplyNo, channel_code)
        logging.info(f"借款返回的查询参数是：{jk_success_resp}")

    with allure.step("借款成功断言"):
        pass

    with allure.step("生成测试结果"):
        # 生成测试结果
        test_result = {
            "userId": user_id,
            "loanApplyNo": loanApplyNo,
            "fundsCode": funds_code,
            "loanAmount": loan_amt,
            "loanDate": datetime.datetime.now().strftime("%Y-%m-%d"),
            "phoneNumber": mobile_no,
            "userName": user_name,
            "idCard": id_no,
            "bankCard": bank_card_no
        }
        # 输出测试结果 - 确保只输出一行
        print(f"TEST_RESULT:{json.dumps(test_result, ensure_ascii=False)}")


# API全流程-哈密众邦D0批扣还款成功
@pytest.mark.run(order=11)
@allure.epic("360沙盒渠道-哈密众邦资方-API全流程")
@allure.feature("360沙盒渠道-还款模块-API全流程")
@allure.title("360沙盒渠道-到期D0还款成功-API全流程")
@allure.story("360沙盒渠道-哈密众邦资方还款案例-API全流程")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.skip()
def test_zb_repay_d0_success_api_flow(get_channel):
    with allure.step("数据初始化"):
        api = core_api_flow_api()
        enc = encrypt_decrypt()
        credit_apply_no = get_credit_apply_no()
        db = Update_Sql_Result()
        apply_time = get_time_stand_api()
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        bank_card_no = get_baofu_ccb_num()
        user_id = get_cust_id()
        certificationApplyNo = get_api_bk_id()
        logging = Logger().init_logger()

        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：哈密众邦  ==  ZB
        loanApplyNo = get_req_seq_no("ZB")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "HAMI_ZHONGBANG"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = get_channel
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "KN_HALF"
        logging.info(f"开始执行测试方法中渠道 {channel_code} 的测试")

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds(channel_code)

    # with allure.step("更新为MOCK环境"):
    #     Update_Sql_Result().update_sushang_zjly_mock()

    with allure.step("用户撞库"):
        # 撞库数据,以手机号为主
        zk_need_encry_data = {"params": {"md5": enc.param_encry_by_md5(mobile_no), "mode": "M"}}
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
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209185"},
                              "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                               "userName": user_name, "bankCardNo": bank_card_no},
                              "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"},
                              "companyInfo": {
                                  "companyName": "中国建筑集团有限公司",
                                  "province": "110000",
                                  "city": "110100",
                                  "district": "110108",
                                  "companyAddr": "北京市海淀区三里河路15号"},
                              "agreementTime": apply_time}
        logging.info(f"{json_dumps_cn(sx_need_encry_data)}")
        # 加密授信数据
        sx_encry_data = api.api_param_encry(sx_need_encry_data, channel_code)
        # 发送授信申请请求
        sx_resp = api.test_apply_credit(sx_encry_data)
        # 授信结果解密
        sx_decry_data = api.api_param_decry(sx_resp)
        partner_creditNo = sx_decry_data["partnerCreditNo"]
        logging.info(f"解密后的授信申请返回结果为：======{sx_decry_data}")

    with allure.step("更新授信相关表为哈密众邦资方"):
        db.update_api_flow_all_table(funds_code, user_id)
        logging.info(f"数据库更新资方完毕")
        time.sleep(5)

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "creditApplyNo": credit_apply_no}
        # 发起授信结果轮询请求
        resp = loop_result().loop_api_flow_sx_result(sx_cx_data, credit_apply_no, channel_code)
        logging.info(f"当前授信结果返回数据为：{resp}")

    with allure.step("绑卡申请"):
        # 请求鉴权数据
        bk_jq_need_encry_data = {"userId": user_id, "certificationApplyNo": certificationApplyNo, "bankCode": "0004",
                                 "idCardNo": id_no, "userMobile": mobile_no, "userName": user_name,
                                 "bankCardNo": bank_card_no, "registerMobile": mobile_no, "agreementTime": apply_time}
        # 绑卡轮询，并且绑卡两次
        with allure.step("第一次绑卡"):
            if channel_code in channel_codes:
                bk_jq_need_encry_data["bindType"] = "fundsChannel"
            else:
                pass
            loop_result().loop_api_flow_bk_result(bk_jq_need_encry_data, channel_code)
        with allure.step("第二次绑卡"):
            if channel_code in channel_codes:
                bk_jq_need_encry_data["bindType"] = "payChannel"
            else:
                pass
            # 第二次绑卡需要更新申请号以及时间，从新赋值
            time.sleep(2)
            bk_jq_need_encry_data["certificationApplyNo"], bk_jq_need_encry_data[
                "agreementTime"] = get_api_bk_id(), get_time_stand_api()
            loop_result().loop_api_flow_bk_result(bk_jq_need_encry_data, channel_code)

    with allure.step("借款试算"):
        # 借款试算数据
        # 加密借款试算数据
        # 发起借款试算请求
        # 解密试算返回结果
        pass

    with allure.step("借款申请"):
        # 借款申请数据
        jk_sq_need_encry_data = {"loanTime": apply_time, "productCode": product_code, "repayMethod": "01",
                                 "loanPurpose": "05", "partnerCreditNo": partner_creditNo, "term": reqPeriods,
                                 "loanAmt": loan_amt, "loanApplyNo": loanApplyNo, "userId": user_id,
                                 "agreementTime": apply_time,
                                 "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no},
                                 "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                                 "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209185"},
                                 "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"}}
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
        jk_success_resp = loop_result().loop_api_flow_loan_result(loan_query_need_encry_data, loanApplyNo, channel_code)
        logging.info(f"借款成功返回的查询参数是：{jk_success_resp}")

    with allure.step("修改api还款相关表"):
        # 修改api还款计划表以便于D0批扣还款
        time.sleep(1)
        db.update_api_flow_zx_loan_plan_info_d0(loanApplyNo, "1")
        db.update_api_flow_zx_loan_note_info_d0(loanApplyNo)
        logging.info(f"修改api还款计划表、借据信息表成功")

    with allure.step("修改批发还款相关表"):
        # 修改批发路由还款计划表以便于D0批扣还款
        db.update_api_core_fr_api_repayment_plan_d0(loanApplyNo, "1")
        db.update_api_core_fr_api_order_info_d0(loanApplyNo)
        logging.info(f"修改批发还款计划表、API订单表成功")

    with allure.step("轮询执行D0批扣还款成功"):
        # 执行api侧D0批扣任务
        time.sleep(1)
        execute_xxl_job().new_cy_batch_d0_repay_apply()
        logging.info(f"执行D0批扣任务成功！请稍等！")
        loop_result().loop_api_flow_repay_result(loanApplyNo)

    with allure.step("还款成功断言"):
        pass

    with allure.step("生成测试结果"):
        # 生成测试结果
        test_result = {
            "userId": user_id,
            "loanApplyNo": loanApplyNo,
            "fundsCode": funds_code,
            "loanAmount": loan_amt,
            "loanDate": datetime.datetime.now().strftime("%Y-%m-%d"),
            "phoneNumber": mobile_no,
            "userName": user_name,
            "idCard": id_no,
            "bankCard": bank_card_no
        }
        print(f"TEST_RESULT:{json.dumps(test_result, ensure_ascii=False)}")

# API全流程-哈密众邦主动还款成功
@pytest.mark.run(order=11)
@allure.epic("360沙盒渠道-哈密众邦资方-API全流程")
@allure.feature("360沙盒渠道-还款模块-API全流程")
@allure.title("360沙盒渠道-到期主动还款成功-API全流程")
@allure.story("360沙盒渠道-哈密众邦资方还款案例-API全流程")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.skip()
def test_zb_repay_success_api_flow(get_channel):
    with allure.step("数据初始化"):
        # 核心api的基类
        api = core_api_flow_api()
        # 加解密基类
        enc = encrypt_decrypt()
        # 随机借据授信申请流水号
        credit_apply_no = get_credit_apply_no()
        # 数据库更新基类
        db = Update_Sql_Result()
        # 当前标准时间
        apply_time = get_time_stand_api()
        # 数据库查询基类
        select_db = Select_Sql_Result()
        # 身份证生成
        id_no, birthday = get_zx_user_id_no()
        # 用户名生成
        user_name = get_user_name()
        # 宝付规则卡号生成
        bank_card_no = get_baofu_ccb_num()
        # custID生成
        user_id = get_cust_id()
        # 绑卡ID生成
        certificationApplyNo = get_api_bk_id()
        # 日志基类
        logging = Logger().init_logger()
        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()
        # 修改对应的缩写或其他标志：哈密众邦  ==  ZB
        loanApplyNo = get_req_seq_no("ZB")
        repayApplyNo = get_credit_apply_no("REPAY")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "HAMI_ZHONGBANG"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = get_channel
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = "12"
        # 产品信息
        product_code = "KN_HALF"

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds(channel_code)

    # with allure.step("更新为MOCK环境"):
    #     Update_Sql_Result().update_sushang_zjly_mock()

    with allure.step("用户撞库"):
        # 撞库数据,以手机号为主
        zk_need_encry_data = {"params": {"md5": enc.param_encry_by_md5(mobile_no), "mode": "M"}}
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
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209185"},
                              "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                               "userName": user_name, "bankCardNo": bank_card_no},
                              "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"},
                              "companyInfo": {
                                  "companyName": "中国建筑集团有限公司",
                                  "province": "110000",
                                  "city": "110100",
                                  "district": "110108",
                                  "companyAddr": "北京市海淀区三里河路15号"},
                              "agreementTime": apply_time}
        logging.info(f"{json_dumps_cn(sx_need_encry_data)}")
        # 加密授信数据
        sx_encry_data = api.api_param_encry(sx_need_encry_data, channel_code)
        # 发送授信申请请求
        sx_resp = api.test_apply_credit(sx_encry_data)
        # 授信结果解密
        sx_decry_data = api.api_param_decry(sx_resp)
        partner_creditNo = sx_decry_data["partnerCreditNo"]
        logging.info(f"解密后的授信申请返回结果为：======{sx_decry_data}")

    with allure.step("更新授信相关表为哈密众邦资方"):
        db.update_api_flow_all_table(funds_code, user_id)
        logging.info(f"数据库更新资方完毕")
        time.sleep(5)

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "creditApplyNo": credit_apply_no}
        # 发起授信结果轮询请求
        resp = loop_result().loop_api_flow_sx_result(sx_cx_data, credit_apply_no, channel_code)
        logging.info(f"当前授信结果返回数据为：{resp}")

    with allure.step("绑卡申请"):
        # 请求鉴权数据
        bk_jq_need_encry_data = {"userId": user_id, "certificationApplyNo": certificationApplyNo, "bankCode": "0004",
                                 "idCardNo": id_no, "userMobile": mobile_no, "userName": user_name,
                                 "bankCardNo": bank_card_no, "registerMobile": mobile_no, "agreementTime": apply_time}
        # 绑卡轮询，并且绑卡两次
    with allure.step("第一次绑卡"):
        if channel_code in channel_codes:
            bk_jq_need_encry_data["bindType"] = "fundsChannel"
        else:
            pass
        loop_result().loop_api_flow_bk_result(bk_jq_need_encry_data, channel_code)
    with allure.step("第二次绑卡"):
        if channel_code in channel_codes:
            bk_jq_need_encry_data["bindType"] = "payChannel"
        else:
            pass
        # 第二次绑卡需要更新申请号以及时间，从新赋值
        time.sleep(2)
        bk_jq_need_encry_data["certificationApplyNo"], bk_jq_need_encry_data[
            "agreementTime"] = get_api_bk_id(), get_time_stand_api()
        loop_result().loop_api_flow_bk_result(bk_jq_need_encry_data, channel_code)

    with allure.step("借款试算"):
        # 借款试算数据
        # 加密借款试算数据
        # 发起借款试算请求
        # 解密试算返回结果
        pass

    with allure.step("借款申请"):
        # 借款申请数据
        jk_sq_need_encry_data = {"loanTime": apply_time, "productCode": product_code, "repayMethod": "01",
                                 "loanPurpose": "05", "partnerCreditNo": partner_creditNo, "term": reqPeriods,
                                 "loanAmt": loan_amt, "loanApplyNo": loanApplyNo, "userId": user_id,
                                 "agreementTime": apply_time,
                                 "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no, "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no},
                                 "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                                 "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209185"},
                                 "geoInfo": {"latitude": "43.57687931900941", "longitude": "112.55172012515888"}}
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
        jk_success_resp = loop_result().loop_api_flow_loan_result(loan_query_need_encry_data, loanApplyNo, channel_code)
        logging.info(f"借款成功返回的查询参数是：{jk_success_resp}")

    with allure.step("修改api还款相关表"):
        # 修改api还款计划表以便于D0批扣还款
        time.sleep(1)
        db.update_api_flow_zx_loan_plan_info_d0(loanApplyNo, "1")
        db.update_api_flow_zx_loan_note_info_d0(loanApplyNo)
        logging.info(f"修改api还款计划表、借据信息表成功")

    with allure.step("修改批发还款相关表"):
        # 修改批发路由还款计划表以便于D0批扣还款
        db.update_api_core_fr_api_repayment_plan_d0(loanApplyNo, "1")
        db.update_api_core_fr_api_order_info_d0(loanApplyNo)
        logging.info(f"修改批发还款计划表、API订单表成功")

    with allure.step("查询相关表取数"):
        # 查询合作方借款流水(合作方内部借款申请单号，多用于问题排查)
        partnerLoanNo = select_db.select_partner_loan_no_apply_record(loanApplyNo)
        # 查询支付通道、共享协议号，取资方绑卡的那条记录
        pmcCode, sharePayAgreementId = select_db.select_greement_id_pay_channel(user_id)

    with allure.step("还款计划查询"):
        plan_query_data = {"userId": user_id, "loanApplyNo": loanApplyNo, "partnerLoanNo": partnerLoanNo}
        # 加密还款计划查询数据
        plan_query_encry_data = api.api_param_encry(plan_query_data, channel_code)
        # 发送还款计划查询请求
        plan_query_resp = api.test_query_loan_plan(plan_query_encry_data)
        # 解密还款计划查询返回数据
        plan_query_decry_data = api.api_param_decry(plan_query_resp)
        logging.info(f"还款计划查询返回数据结果为：======={plan_query_decry_data}")

    with allure.step("还款试算"):
        # type：1 按期还款  2 提前还款  3 按金额还款
        repay_try_need_encry_data = {"userId": user_id, "repayApplyNo": repayApplyNo,
                                     "loanApplyNo": loanApplyNo, "partnerLoanNo": partnerLoanNo,
                                     "repayType": "2", "repayTime": apply_time}
        print(repay_try_need_encry_data)
        # 加密还款试算数据
        repay_try_encry_data = api.api_param_encry(repay_try_need_encry_data, channel_code)
        # 发送还款试算请求
        repay_try_resp = api.test_repay_trial(repay_try_encry_data)
        # 解密还款试算返回数据
        repay_try_decry_data = api.api_param_decry(repay_try_resp)
        logging.info(f"试算返回数据结果为：======={repay_try_decry_data}")

    with allure.step("主动还款"):
        # 主动还款数据
        repay_need_encry_data = {"userId": user_id, "repayApplyNo": repayApplyNo,
                                 "loanApplyNo": loanApplyNo, "partnerLoanNo": partnerLoanNo,
                                 "repayType": "2", "repayMethod": "0", "repayTime": apply_time, "withholdFlag": "Y",
                                 "bankCardInfo": {"bankCode": "0004", "idCardNo": id_no,
                                                  "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no,
                                                  "sharePayAgreementId": sharePayAgreementId,
                                                  "pmcCode": pmcCode}}
        # 加密还款数据
        repay_encry_data = api.api_param_encry(repay_need_encry_data, channel_code)
        # 发送试算请求
        repay_resp = api.test_apply_repayment(repay_encry_data)
        # 解密还款返回数据
        repay_decry_data = api.api_param_decry(repay_resp)
        logging.info(f"查询返回数据结果为：======={repay_decry_data}")

    with allure.step("执行单笔还款处理任务"):
        execute_xxl_job().single_repay()

    with allure.step("执行单笔还款查询任务"):
        time.sleep(15)
        execute_xxl_job().single_query_result()

    with allure.step("查询还款结果"):
        time.sleep(15)
        # 查询还款数据
        repay_query_need_encry_data = {"userId": user_id, "repayApplyNo": repayApplyNo}
        # 加密还款查询数据
        repay_query_encry_data = api.api_param_encry(repay_query_need_encry_data, channel_code)
        # 发送查询请求
        repay_query_resp = api.test_query_repay_result(repay_query_encry_data)
        # 解密查询返回数据
        repay_query_decry_data = api.api_param_decry(repay_query_resp)
        logging.info(f"查询返回数据结果为：======={repay_query_decry_data}")

    
    with allure.step("还款成功断言"):
        pass    

    with allure.step("生成测试结果"):
        # 生成测试结果
        test_result = {
            "userId": user_id,
            "loanApplyNo": loanApplyNo,
            "fundsCode": funds_code,
            "loanAmount": loan_amt,
            "loanDate": datetime.datetime.now().strftime("%Y-%m-%d"),
            "phoneNumber": mobile_no,
            "userName": user_name,
            "idCard": id_no,
            "bankCard": bank_card_no
        }
        print(f"TEST_RESULT:{json.dumps(test_result, ensure_ascii=False)}")
