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
from util_tools.Xxl_Job_Executor import execute_xxl_job
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Api_Flow_Api import core_api_flow_api
from common.Encrypt_Decrypt import encrypt_decrypt
from util_tools.Read_photo import *
from util_tools.Read_Yaml import read_risk_phone
from common.Update_Database_Result import Update_Sql_Result
from util_tools.Loop_result import loop_result


# API全流程-中原提钱花放款成功
@pytest.mark.run(order=10)
@allure.epic("360沙盒渠道-中原提钱花资方-API全流程")
@allure.feature("360沙盒渠道-授信模块-API全流程")
@allure.title("360沙盒渠道-借款成功-API全流程")
@allure.story("360沙盒渠道-中原提钱花资方授信案例-API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_zy_loan_success_api_flow(get_channel,get_loan_perid):
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
        # 还款流水号
        repayApplyNo = get_credit_apply_no("REPAY")
        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()

        # 修改对应的缩写或其他标志：中原提钱花  ==  ZY
        loanApplyNo = get_req_seq_no("ZY")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "ZHONG_YUAN"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = get_channel
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = get_loan_perid
        # 产品信息
        product_code = "KN_HALF"
        logging.info(f"开始执行测试方法中渠道 {channel_code} 的测试")

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds(channel_code)

    with allure.step("更新为MOCK环境"):
        Update_Sql_Result().update_zytqh_zjly_mock()

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
                                                "nameOCR": user_name, "idCardNoOCR": id_no, "beginTimeOCR": "20170829",
                                                "duetimeOCR": "20370829",
                                                "addressOCR": "黑龙江省哈尔滨市松北区成钧街道豪承小区190号楼501",
                                                "sexOCR": "M", "ethnicOCR": "汉族", "issueOrgOCR": "黑龙江公安局"},
                              "faceInfo": {"assayTime": apply_time, "assayType": "SENSETIME", "best": get_best_photo()},
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209188"},
                              "bankCardInfo": {"bankCode": "0003", "idCardNo": id_no, "userMobile": mobile_no,
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

    with allure.step("更新授信相关表为中原提钱花资方"):
        db.update_api_flow_all_table(funds_code, user_id)
        logging.info(f"数据库更新资方完毕")
        time.sleep(5)

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "creditApplyNo": credit_apply_no}
        # 发起授信结果轮询请求
        resp = loop_result().loop_api_flow_sx_result(sx_cx_data, credit_apply_no, channel_code)
        logging.info(f"当前授信结果返回数据为：{resp}")

    with allure.step("推送客户中心"):
        execute_xxl_job().push_credit_info_to_customer_center(credit_apply_no)
        time.sleep(5)
        logging.info("授信成功后推送客户中心成功！")

    with allure.step("绑卡申请"):
        # 请求鉴权数据
        bk_jq_need_encry_data = {"userId": user_id, "certificationApplyNo": certificationApplyNo, "bankCode": "0003",
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

    with allure.step("借款申请"):
        # 借款申请数据
        jk_sq_need_encry_data = {"loanTime": apply_time, "productCode": product_code, "repayMethod": "01",
                                 "loanPurpose": "05", "partnerCreditNo": partner_creditNo, "term": reqPeriods,
                                 "loanAmt": loan_amt, "loanApplyNo": loanApplyNo, "userId": user_id,
                                 "agreementTime": apply_time,
                                 "bankCardInfo": {"bankCode": "0003", "idCardNo": id_no, "userMobile": mobile_no,
                                                  "userName": user_name, "bankCardNo": bank_card_no},
                                 "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                                 "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209188"},
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
            "bankCard": bank_card_no,
            "loanPeriod": reqPeriods
        }   
        # 输出测试结果 - 确保只输出一行
        print(f"TEST_RESULT:{json.dumps(test_result, ensure_ascii=False)}")


# API全流程-中原提钱花授信成功
@pytest.mark.run(order=10)
@allure.epic("360沙盒渠道-中原提钱花资方-API全流程")
@allure.feature("360沙盒渠道-授信模块-API全流程")
@allure.title("360沙盒渠道-授信成功-API全流程")
@allure.story("360沙盒渠道-中原提钱花资方授信案例-API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_zy_credit_success_api_flow(get_channel,get_loan_perid):
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
        # 还款流水号
        repayApplyNo = get_credit_apply_no("REPAY")
        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()

        # 修改对应的缩写或其他标志：中原提钱花  ==  ZY
        loanApplyNo = get_req_seq_no("ZY")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "ZHONG_YUAN"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = get_channel
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = get_loan_perid
        # 产品信息
        product_code = "KN_HALF"
        logging.info(f"开始执行测试方法中渠道 {channel_code} 的测试")

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds(channel_code)

    with allure.step("更新为MOCK环境"):
        Update_Sql_Result().update_zytqh_zjly_mock()

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
                                                "nameOCR": user_name, "idCardNoOCR": id_no, "beginTimeOCR": "20170829",
                                                "duetimeOCR": "20370829",
                                                "addressOCR": "黑龙江省哈尔滨市松北区成钧街道豪承小区190号楼501",
                                                "sexOCR": "M", "ethnicOCR": "汉族", "issueOrgOCR": "黑龙江公安局"},
                              "faceInfo": {"assayTime": apply_time, "assayType": "SENSETIME", "best": get_best_photo()},
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209188"},
                              "bankCardInfo": {"bankCode": "0003", "idCardNo": id_no, "userMobile": mobile_no,
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

    with allure.step("更新授信相关表为中原提钱花资方"):
        db.update_api_flow_all_table(funds_code, user_id)
        logging.info(f"数据库更新资方完毕")
        time.sleep(5)

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "creditApplyNo": credit_apply_no}
        # 发起授信结果轮询请求
        resp = loop_result().loop_api_flow_sx_result(sx_cx_data, credit_apply_no, channel_code)
        logging.info(f"当前授信结果返回数据为：{resp}")

    with allure.step("推送客户中心"):
        execute_xxl_job().push_credit_info_to_customer_center(credit_apply_no)
        time.sleep(5)
        logging.info("授信成功后推送客户中心成功！")

    with allure.step("授信成功断言"):
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
            "bankCard": bank_card_no,
            "loanPeriod": reqPeriods
        }   
        # 输出测试结果 - 确保只输出一行
        print(f"TEST_RESULT:{json.dumps(test_result, ensure_ascii=False)}")


# API全流程-中原提钱花绑卡成功
@pytest.mark.run(order=10)
@allure.epic("360沙盒渠道-中原提钱花资方-API全流程")
@allure.feature("360沙盒渠道-授信模块-API全流程")
@allure.title("360沙盒渠道-绑卡成功-API全流程")
@allure.story("360沙盒渠道-中原提钱花资方授信案例-API全流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_zy_band_card_success_api_flow(get_channel,get_loan_perid):
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
        # 还款流水号
        repayApplyNo = get_credit_apply_no("REPAY")
        # 获取风控加白了的手机号，读取本地txt文件
        mobile_no = read_risk_phone()

        # 修改对应的缩写或其他标志：中原提钱花  ==  ZY
        loanApplyNo = get_req_seq_no("ZY")
        # 资金方，修改成对应需要放款的资金方funds_code
        funds_code = "ZHONG_YUAN"
        # 渠道方，修改成对应需要走的渠道方channel_code
        channel_code = get_channel
        # 借款金额
        loan_amt = "2000"
        # 借款期数
        reqPeriods = get_loan_perid
        # 产品信息
        product_code = "KN_HALF"
        logging.info(f"开始执行测试方法中渠道 {channel_code} 的测试")

    with allure.step("更新为限流模式"):
        Update_Sql_Result().update_api_chanel_non_funds(channel_code)

    with allure.step("更新为MOCK环境"):
        Update_Sql_Result().update_zytqh_zjly_mock()

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
                                                "nameOCR": user_name, "idCardNoOCR": id_no, "beginTimeOCR": "20170829",
                                                "duetimeOCR": "20370829",
                                                "addressOCR": "黑龙江省哈尔滨市松北区成钧街道豪承小区190号楼501",
                                                "sexOCR": "M", "ethnicOCR": "汉族", "issueOrgOCR": "黑龙江公安局"},
                              "faceInfo": {"assayTime": apply_time, "assayType": "SENSETIME", "best": get_best_photo()},
                              "linkmanInfo": {"relationshipA": "10", "nameA": "毋琳子", "phoneA": "15161455378",
                                              "relationshipB": "60", "nameB": "花娥茜", "phoneB": "15982209188"},
                              "bankCardInfo": {"bankCode": "0003", "idCardNo": id_no, "userMobile": mobile_no,
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

    with allure.step("更新授信相关表为中原提钱花资方"):
        db.update_api_flow_all_table(funds_code, user_id)
        logging.info(f"数据库更新资方完毕")
        time.sleep(5)

    with allure.step("轮询判断是否授信成功"):
        # 授信查询数据
        sx_cx_data = {"userId": user_id, "creditApplyNo": credit_apply_no}
        # 发起授信结果轮询请求
        resp = loop_result().loop_api_flow_sx_result(sx_cx_data, credit_apply_no, channel_code)
        logging.info(f"当前授信结果返回数据为：{resp}")

    with allure.step("推送客户中心"):
        execute_xxl_job().push_credit_info_to_customer_center(credit_apply_no)
        time.sleep(5)
        logging.info("授信成功后推送客户中心成功！")

    with allure.step("绑卡申请"):
        # 请求鉴权数据
        bk_jq_need_encry_data = {"userId": user_id, "certificationApplyNo": certificationApplyNo, "bankCode": "0003",
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

    with allure.step("绑卡成功断言"):
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
            "bankCard": bank_card_no,
            "loanPeriod": reqPeriods
        }   
        # 输出测试结果 - 确保只输出一行
        print(f"TEST_RESULT:{json.dumps(test_result, ensure_ascii=False)}")

