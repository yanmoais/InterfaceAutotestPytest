#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午4:03

"""
    此文件自动化案例为各个资金方授信-借款-还款流程
"""
import json

from testdata.assert_data.banding_assert_data import banding_card_assert_data
from testdata.assert_data.loan_assert_data import *
from testdata.assert_data.loan_credit_amt_assert_data import credit_amt_query_success_data
from util_tools.Loop_result import loop_result
from util_tools.Public_Assert import banding_card_success_assert, loan_success_assert, loan_credit_amt_success_assert
from util_tools.logger import Logger
from util_tools.Faker import *
import time
import jsonpath
from common.Base_API import Base_Api
from common.Core_Zjly_Api import core_zjly_api
from common.Encrypt_Decrypt import encrypt_decrypt
import allure


@allure.epic("海峡资方")
@allure.feature("授信模块")
@allure.story("海峡资方授信放款案例")
@allure.title("授信成功")
def test_haixia_credit_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_user_idNo()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        loan_no = get_loan_no()
        bank_name = "福建海峡银行股份有限公司"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        fk_no = get_fk_id()
        contract_no = get_contract_no()
        dbht_no = get_dbht_no()
        bink_no = get_bink_no()
        logging = Logger().init_logger()

    # 每次请求前需要进行加密，得到的返回结果需要传给下游接口时候需要解密出来，下次使用又需要加密
    with allure.step("发起授信"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'HX_TEST', 'params':json_dumps_cn({"birthday":birthday,"loanNo":loan_no,"guaranteeInfo":{"guarOdIntRate":"0.00022037","guarRate":"0.079333","guarTime":"12","guarAmt":"237.96"},"nation":"汉","loanseqno":loan_sqe_no,"idNo":id_no,"merchantName":"大商户","monthlySalary":"1000","idExpireDate":"2037-11-30","merchantId":"69355551222","companyPhone":"02061959111","childrenNum":"2","custId":custid,"fromChannel":"01","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"applyDt":"2024-09-04","emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"idStartDate":"2017-11-30","signOffice":"罗定市公安局","mobileNo":mobile_no,"userName":user_name,"fileIDs":"5ff341cdeeed46d98f8cc599a4c72c401718942716298,b368245bc9b24ddeae9116ba2a22e12b1688608942043,e6e60b02818642118986b9be415ad0f71688616059531,bc5cfb353801470d9ce96eaff7f9e9581688621835451,562d6907777740f48511cc21977ffe811688621899067,b42f1234c98846079570799d87a94c671688714949013,1b9d43f6dee840dcbb2f7358c87ff6f11689059737364","occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"maxDegree":"10","accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0102","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0102","bankName":"福建海峡银行股份有限公司","acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}],"maritalStatus":"10"}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'haiXia')
        print("加密的数据是==================", sx_encry_data)
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'haiXia')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "HX_TEST","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data, 'haiXia')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry, 'haiXia')

    with allure.step("授信成功断言"):
        loan_success_assert(loan_sqe_no, credit_success_assert_data)


@allure.epic("海峡资方")
@allure.feature("授信模块")
@allure.story("海峡资方授信放款案例")
@allure.title("授信额度查询成功")
def test_haixia_credit_amt_query_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_user_idNo()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        loan_no = get_loan_no()
        bank_name = "福建海峡银行股份有限公司"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        fk_no = get_fk_id()
        contract_no = get_contract_no()
        dbht_no = get_dbht_no()
        bink_no = get_bink_no()
        logging = Logger().init_logger()

    # 每次请求前需要进行加密，得到的返回结果需要传给下游接口时候需要解密出来，下次使用又需要加密
    with allure.step("发起授信"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'HX_TEST', 'params':json_dumps_cn({"birthday":birthday,"loanNo":loan_no,"guaranteeInfo":{"guarOdIntRate":"0.00022037","guarRate":"0.079333","guarTime":"12","guarAmt":"237.96"},"nation":"汉","loanseqno":loan_sqe_no,"idNo":id_no,"merchantName":"大商户","monthlySalary":"1000","idExpireDate":"2037-11-30","merchantId":"69355551222","companyPhone":"02061959111","childrenNum":"2","custId":custid,"fromChannel":"01","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"applyDt":"2024-09-04","emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"idStartDate":"2017-11-30","signOffice":"罗定市公安局","mobileNo":mobile_no,"userName":user_name,"fileIDs":"5ff341cdeeed46d98f8cc599a4c72c401718942716298,b368245bc9b24ddeae9116ba2a22e12b1688608942043,e6e60b02818642118986b9be415ad0f71688616059531,bc5cfb353801470d9ce96eaff7f9e9581688621835451,562d6907777740f48511cc21977ffe811688621899067,b42f1234c98846079570799d87a94c671688714949013,1b9d43f6dee840dcbb2f7358c87ff6f11689059737364","occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"maxDegree":"10","accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0102","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0102","bankName":"福建海峡银行股份有限公司","acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}],"maritalStatus":"10"}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'haiXia')
        print("加密的数据是==================", sx_encry_data)
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'haiXia')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "HX_TEST","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data, 'haiXia')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry, 'haiXia')

    with allure.step("发起借款"):
        # 5.放款申请加密
        fk_encry_data = {"apiKey":"HX_TEST","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no,"bindid":bink_no,"amt":loan_amt,"guarAmt":"237.96","guarRate":"0.079333","guarTime":"12","guarOdIntRate":"0.00022037","guarSignTime":"2024-09-07","guarEndTime":"2025-09-07","guarContNo":dbht_no,"guarContAddr":"广东","contractNo":contract_no,"fileIDs":"1780487717038329856,6b2a97dc90794fe2b78fa5412c82be581713337050255","accInfoDto":{"acctKind":"01","acctTyp":"01","acctBankCode":"0102","acct_no":acct_no,"acctName":user_name,"id_no":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮","bankName":"福建海峡银行股份有限公司"},"guaranteeList":[{"perdNo":"1","guarDate":"2024-10-07","perGuarFee":"19.83"},{"perdNo":"2","guarDate":"2024-11-07","perGuarFee":"19.83"},{"perdNo":"3","guarDate":"2024-12-07","perGuarFee":"19.83"},{"perdNo":"4","guarDate":"2025-01-07","perGuarFee":"19.83"},{"perdNo":"5","guarDate":"2025-02-07","perGuarFee":"19.83"},{"perdNo":"6","guarDate":"2025-03-07","perGuarFee":"19.83"},{"perdNo":"7","guarDate":"2025-04-07","perGuarFee":"19.83"},{"perdNo":"8","guarDate":"2025-05-07","perGuarFee":"19.83"},{"perdNo":"9","guarDate":"2025-06-07","perGuarFee":"19.83"},{"perdNo":"10","guarDate":"2025-07-07","perGuarFee":"19.83"},{"perdNo":"11","guarDate":"2025-08-07","perGuarFee":"19.83"},{"perdNo":"12","guarDate":"2025-09-07","perGuarFee":"19.83"}]}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的放款申请数据为：======{fk_encry_data}")
        fksq_encry = encrypt_decrypt().param_encry_by_channel(fk_encry_data, 'haiXia')
        logging.info(f"加密后的放款申请数据为：======{fksq_encry}")
        # 5.放款申请请求
        fksq_resp = core_zjly_api().test_loan_apply_settle(fksq_encry)
        # 5.放款申请返回数据解密
        fksq_decry = encrypt_decrypt().param_decrys_by_channel(fksq_resp, 'haiXia')
        logging.info(f"解密后的放款申请返回数据为：======{fksq_decry}")

    with allure.step("借款状态查询"):
        # 6.放款状态查询加密
        fkzt_encry_data = {"apiKey": "HX_TEST","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        fkzt_encry = encrypt_decrypt().param_encry_by_channel(fkzt_encry_data, 'haiXia')
        logging.info(f"加密后的放款状态数据为：======{fkzt_encry}")
        # 轮询查询放款结果，查询到结果为"放款成功"则跳出
        # 6.放款状态查询请求
        loop_result().loop_fkcx_result(fkzt_encry, 'haiXia')

    with allure.step("授信额度断言"):
        loan_credit_amt_success_assert(loan_sqe_no, credit_amt_query_success_data)


@allure.epic("海峡资方")
@allure.feature("授信模块")
@allure.story("海峡资方授信放款案例")
@allure.title("放款成功")
def test_haixia_loan_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_user_idNo()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        loan_no = get_loan_no()
        bank_name = "福建海峡银行股份有限公司"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        fk_no = get_fk_id()
        contract_no = get_contract_no()
        dbht_no = get_dbht_no()
        bink_no = get_bink_no()
        logging = Logger().init_logger()

    # 每次请求前需要进行加密，得到的返回结果需要传给下游接口时候需要解密出来，下次使用又需要加密
    with allure.step("发起授信"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'HX_TEST', 'params':json_dumps_cn({"birthday":birthday,"loanNo":loan_no,"guaranteeInfo":{"guarOdIntRate":"0.00022037","guarRate":"0.079333","guarTime":"12","guarAmt":"237.96"},"nation":"汉","loanseqno":loan_sqe_no,"idNo":id_no,"merchantName":"大商户","monthlySalary":"1000","idExpireDate":"2037-11-30","merchantId":"69355551222","companyPhone":"02061959111","childrenNum":"2","custId":custid,"fromChannel":"01","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"applyDt":"2024-09-04","emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"idStartDate":"2017-11-30","signOffice":"罗定市公安局","mobileNo":mobile_no,"userName":user_name,"fileIDs":"5ff341cdeeed46d98f8cc599a4c72c401718942716298,b368245bc9b24ddeae9116ba2a22e12b1688608942043,e6e60b02818642118986b9be415ad0f71688616059531,bc5cfb353801470d9ce96eaff7f9e9581688621835451,562d6907777740f48511cc21977ffe811688621899067,b42f1234c98846079570799d87a94c671688714949013,1b9d43f6dee840dcbb2f7358c87ff6f11689059737364","occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"maxDegree":"10","accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0102","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0102","bankName":"福建海峡银行股份有限公司","acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}],"maritalStatus":"10"}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'haiXia')
        print("加密的数据是==================", sx_encry_data)
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'haiXia')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "HX_TEST","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data, 'haiXia')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry, 'haiXia')

    with allure.step("发起借款"):
        # 5.放款申请加密
        fk_encry_data = {"apiKey":"HX_TEST","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no,"bindid":bink_no,"amt":loan_amt,"guarAmt":"237.96","guarRate":"0.079333","guarTime":"12","guarOdIntRate":"0.00022037","guarSignTime":"2024-09-07","guarEndTime":"2025-09-07","guarContNo":dbht_no,"guarContAddr":"广东","contractNo":contract_no,"fileIDs":"1780487717038329856,6b2a97dc90794fe2b78fa5412c82be581713337050255","accInfoDto":{"acctKind":"01","acctTyp":"01","acctBankCode":"0102","acct_no":acct_no,"acctName":user_name,"id_no":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮","bankName":"福建海峡银行股份有限公司"},"guaranteeList":[{"perdNo":"1","guarDate":"2024-10-07","perGuarFee":"19.83"},{"perdNo":"2","guarDate":"2024-11-07","perGuarFee":"19.83"},{"perdNo":"3","guarDate":"2024-12-07","perGuarFee":"19.83"},{"perdNo":"4","guarDate":"2025-01-07","perGuarFee":"19.83"},{"perdNo":"5","guarDate":"2025-02-07","perGuarFee":"19.83"},{"perdNo":"6","guarDate":"2025-03-07","perGuarFee":"19.83"},{"perdNo":"7","guarDate":"2025-04-07","perGuarFee":"19.83"},{"perdNo":"8","guarDate":"2025-05-07","perGuarFee":"19.83"},{"perdNo":"9","guarDate":"2025-06-07","perGuarFee":"19.83"},{"perdNo":"10","guarDate":"2025-07-07","perGuarFee":"19.83"},{"perdNo":"11","guarDate":"2025-08-07","perGuarFee":"19.83"},{"perdNo":"12","guarDate":"2025-09-07","perGuarFee":"19.83"}]}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的放款申请数据为：======{fk_encry_data}")
        fksq_encry = encrypt_decrypt().param_encry_by_channel(fk_encry_data, 'haiXia')
        logging.info(f"加密后的放款申请数据为：======{fksq_encry}")
        # 5.放款申请请求
        fksq_resp = core_zjly_api().test_loan_apply_settle(fksq_encry)
        # 5.放款申请返回数据解密
        fksq_decry = encrypt_decrypt().param_decrys_by_channel(fksq_resp, 'haiXia')
        logging.info(f"解密后的放款申请返回数据为：======{fksq_decry}")

    with allure.step("借款状态查询"):
        # 6.放款状态查询加密
        fkzt_encry_data = {"apiKey": "HX_TEST","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        fkzt_encry = encrypt_decrypt().param_encry_by_channel(fkzt_encry_data, 'haiXia')
        logging.info(f"加密后的放款状态数据为：======{fkzt_encry}")
        # 轮询查询放款结果，查询到结果为"放款成功"则跳出
        # 6.放款状态查询请求
        loop_result().loop_fkcx_result(fkzt_encry, 'haiXia')

    with allure.step("还款计划查询"):
        # 放款成功后需要再次调用一下还款计划接口，落库更新
        # 7.还款计划查询加密
        hkjh_encry_data = {"apiKey":"HX_TEST","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的还款计划查询数据为：======{hkjh_encry_data}")
        hkjh_encry = encrypt_decrypt().param_encry_by_channel(hkjh_encry_data, 'haiXia')
        logging.info(f"加密后的还款计划查询数据为：======{hkjh_encry}")
        # 7.还款计划查询请求
        hkjh_resp = core_zjly_api().test_loan_apply_order_query(hkjh_encry)
        # 7.还款计划查询返回数据解密
        hkjh_decry = encrypt_decrypt().param_decrys_by_channel(hkjh_resp, 'haiXia')
        logging.info(f"解密后的还款计划查询数据为：======{hkjh_decry}")

    with allure.step("放款成功断言"):
        loan_success_assert(loan_sqe_no, loan_success_assert_data)
