#
# -*- coding：utf-8 —*-
# @Author : Blues.Lan
# Them：Pyhon自动化
# @Time :  下午2:46
"""
    此文件自动化案例为各个资金方授信-借款-还款流程
"""
from testdata.assert_data.banding_assert_data import *
from testdata.assert_data.loan_assert_data import *
from testdata.assert_data.loan_credit_amt_assert_data import credit_amt_query_success_data
from util_tools.Loop_result import loop_result
from util_tools.Public_Assert import loan_success_assert, banding_card_success_assert, loan_credit_amt_success_assert
from util_tools.logger import Logger
from util_tools.Faker import *
from common.Core_Zjly_Api import core_zjly_api
from common.Encrypt_Decrypt import encrypt_decrypt
import allure


# 振兴资金方授信成功
@allure.epic("振兴资方")
@allure.feature("授信模块")
@allure.title("授信成功")
@allure.story("振兴资方授信放款案例")
@allure.severity(allure.severity_level.CRITICAL)
def test_zx_credit_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        bank_name = "中国建设银行"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        bk_no = get_bank_id()
        fk_no = get_fk_id()
        logging = Logger().init_logger()

    with allure.step("发起授信/客户信息同步"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'ZLSK-ZX', 'params':json_dumps_cn({"birthday":birthday,"applyDt":"2024-07-04","maxDegree":"10","maritalStatus":"10","idStartDate":"2024-07-18","signOffice":"罗定市公安局","mobileNo":mobile_no,"gender":"F","userName":user_name,"loanseqno":loan_sqe_no,"idNo":id_no,"monthlySalary":"1000","idExpireDate":"9999-12-31","custId":custid,"fromChannel":"01","fileIDs":"a8c06a83a1554ecca27faceb1ed92f5a1689327582151,86a039f4527440bb905fc47ca51a78a31689327582552,a963544b648143f19fd57f79405109511689327582670,7f485a58bc7e492f8bba988d7fd1f2561689327582760,1b1125bd7bdd42e29930b5a64e06c6aa1689327582873,fcf14e96ee7e4dd5a0d747d9683eb1201689327582970,10e462213a5c407cacf2b23dc8933af41689327583096,afc5eea447464782a47f12462b16a60c1689327583885","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}]}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'zhenXing')
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'zhenXing')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data,'zhenXing')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry,'zhenXing')

    with allure.step("授信成功断言"):
        loan_success_assert(loan_sqe_no, credit_success_assert_data)


# 振兴资金方额度查询成功
@allure.epic("振兴资方")
@allure.feature("授信模块")
@allure.title("额度查询成功")
@allure.story("振兴资方授信放款案例")
@allure.severity(allure.severity_level.CRITICAL)
def test_zx_credit_amt_query_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        bank_name = "中国建设银行"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        bk_no = get_bank_id()
        fk_no = get_fk_id()
        logging = Logger().init_logger()

    with allure.step("发起授信/客户信息同步"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'ZLSK-ZX', 'params':json_dumps_cn({"birthday":birthday,"applyDt":"2024-07-04","maxDegree":"10","maritalStatus":"10","idStartDate":"2024-07-18","signOffice":"罗定市公安局","mobileNo":mobile_no,"gender":"F","userName":user_name,"loanseqno":loan_sqe_no,"idNo":id_no,"monthlySalary":"1000","idExpireDate":"9999-12-31","custId":custid,"fromChannel":"01","fileIDs":"a8c06a83a1554ecca27faceb1ed92f5a1689327582151,86a039f4527440bb905fc47ca51a78a31689327582552,a963544b648143f19fd57f79405109511689327582670,7f485a58bc7e492f8bba988d7fd1f2561689327582760,1b1125bd7bdd42e29930b5a64e06c6aa1689327582873,fcf14e96ee7e4dd5a0d747d9683eb1201689327582970,10e462213a5c407cacf2b23dc8933af41689327583096,afc5eea447464782a47f12462b16a60c1689327583885","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}]}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'zhenXing')
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'zhenXing')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data,'zhenXing')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry,'zhenXing')

    with allure.step("发起通联绑卡"):
        # 3.签约申请加密
        qybk_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"seqno":bk_no,"loanseqno":loan_sqe_no,"id_no":id_no,"user_name":user_name,"mobile_no":mobile_no,"bankCode":"0105","cardNo":acct_no,"bankName":bank_name,"registerPhone":mobile_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的签约申请数据为：======{qybk_ency_data}")
        qybk_encry = encrypt_decrypt().param_encry_by_channel(qybk_ency_data, 'zhenXing')
        logging.info(f"加密后的签约申请数据为：======{qybk_encry}")
        # 3.签约申请请求
        qysq_resp = core_zjly_api().test_binding_card_apply(qybk_encry)
        # 3.签约申请返回数据解密
        qysq_decry = encrypt_decrypt().param_decrys_by_channel(qysq_resp,'zhenXing')
        logging.info(f"解密后的签约申请返回数据为：======{qysq_decry}")

    with allure.step("绑卡签约确认"):
        # 4.签约确认加密
        qyqr_encry_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"seqno":bk_no,"smscode":"111111"}),"requestNo": req_no}
        # 需要将数据再次格式化成带转义符并且去除空格
        qyqr_encry = encrypt_decrypt().param_encry_by_channel(qyqr_encry_data,'zhenXing')
        logging.info(f"加密后的签约确认数据为：======{qyqr_encry}")
        # 4.签约确认请求
        qyqr_resp = core_zjly_api().test_binding_card_confirm(qyqr_encry)
        # 4.签约确认返回数据解密
        qyqr_decry = encrypt_decrypt().param_decrys_by_channel(qyqr_resp,'zhenXing')
        logging.info(f"解密后的签约确认返回数据为：======{qyqr_decry}")

    with allure.step("发起借款"):
        # 5.放款申请加密
        fk_encry_data = {"apiKey":"ZLSK-ZX","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no,"amt":loan_amt,"fileIDs":"1780487717038329856,6b2a97dc90794fe2b78fa5412c82be581713337050255","accInfoDto":{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","acct_no":acct_no,"acctName":user_name,"id_no":id_no,"acctPhone":mobile_no,"bankName":bank_name}}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的放款申请数据为：======{fk_encry_data}")
        fksq_encry = encrypt_decrypt().param_encry_by_channel(fk_encry_data, 'zhenXing')
        logging.info(f"加密后的放款申请数据为：======{fksq_encry}")
        # 5.放款申请请求
        fksq_resp = core_zjly_api().test_loan_apply_settle(fksq_encry)
        # 5.放款申请返回数据解密
        fksq_decry = encrypt_decrypt().param_decrys_by_channel(fksq_resp, 'zhenXing')
        logging.info(f"解密后的放款申请返回数据为：======{fksq_decry}")

    with allure.step("借款状态查询"):
        # 6.放款状态查询加密
        fkzt_encry_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        fkzt_encry = encrypt_decrypt().param_encry_by_channel(fkzt_encry_data, 'zhenXing')
        logging.info(f"加密后的放款状态数据为：======{fkzt_encry}")
        # 轮询查询放款结果，查询到结果为"放款成功"则跳出
        # 6.放款状态查询请求
        loop_result().loop_fkcx_result(fkzt_encry, 'zhenXing')

    with allure.step("授信额度断言"):
        loan_credit_amt_success_assert(loan_sqe_no, credit_amt_query_success_data)


# 振兴资金方绑卡成功
@allure.epic("振兴资方")
@allure.feature("授信模块")
@allure.title("绑卡成功")
@allure.story("振兴资方授信放款案例")
@allure.severity(allure.severity_level.CRITICAL)
def test_zx_binding_card_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        bank_name = "中国建设银行"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        bk_no = get_bank_id()
        fk_no = get_fk_id()
        logging = Logger().init_logger()

    with allure.step("发起授信/客户信息同步"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'ZLSK-ZX', 'params':json_dumps_cn({"birthday":birthday,"applyDt":"2024-07-04","maxDegree":"10","maritalStatus":"10","idStartDate":"2024-07-18","signOffice":"罗定市公安局","mobileNo":mobile_no,"gender":"F","userName":user_name,"loanseqno":loan_sqe_no,"idNo":id_no,"monthlySalary":"1000","idExpireDate":"9999-12-31","custId":custid,"fromChannel":"01","fileIDs":"a8c06a83a1554ecca27faceb1ed92f5a1689327582151,86a039f4527440bb905fc47ca51a78a31689327582552,a963544b648143f19fd57f79405109511689327582670,7f485a58bc7e492f8bba988d7fd1f2561689327582760,1b1125bd7bdd42e29930b5a64e06c6aa1689327582873,fcf14e96ee7e4dd5a0d747d9683eb1201689327582970,10e462213a5c407cacf2b23dc8933af41689327583096,afc5eea447464782a47f12462b16a60c1689327583885","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}]}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'zhenXing')
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'zhenXing')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data,'zhenXing')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry,'zhenXing')

    with allure.step("发起通联绑卡"):
        # 3.签约申请加密
        qybk_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"seqno":bk_no,"loanseqno":loan_sqe_no,"id_no":id_no,"user_name":user_name,"mobile_no":mobile_no,"bankCode":"0105","cardNo":acct_no,"bankName":bank_name,"registerPhone":mobile_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的签约申请数据为：======{qybk_ency_data}")
        qybk_encry = encrypt_decrypt().param_encry_by_channel(qybk_ency_data, 'zhenXing')
        logging.info(f"加密后的签约申请数据为：======{qybk_encry}")
        # 3.签约申请请求
        qysq_resp = core_zjly_api().test_binding_card_apply(qybk_encry)
        # 3.签约申请返回数据解密
        qysq_decry = encrypt_decrypt().param_decrys_by_channel(qysq_resp,'zhenXing')
        logging.info(f"解密后的签约申请返回数据为：======{qysq_decry}")

    with allure.step("绑卡签约确认"):
        # 4.签约确认加密
        qyqr_encry_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"seqno":bk_no,"smscode":"111111"}),"requestNo": req_no}
        # 需要将数据再次格式化成带转义符并且去除空格
        qyqr_encry = encrypt_decrypt().param_encry_by_channel(qyqr_encry_data,'zhenXing')
        logging.info(f"加密后的签约确认数据为：======{qyqr_encry}")
        # 4.签约确认请求
        qyqr_resp = core_zjly_api().test_binding_card_confirm(qyqr_encry)
        # 4.签约确认返回数据解密
        qyqr_decry = encrypt_decrypt().param_decrys_by_channel(qyqr_resp,'zhenXing')
        logging.info(f"解密后的签约确认返回数据为：======{qyqr_decry}")

    with allure.step("绑卡成功断言"):
        banding_card_success_assert(bk_no, banding_card_assert_data)


@allure.epic("振兴资方")
@allure.feature("授信模块")
@allure.story("振兴资方授信放款案例")
@allure.title("放款成功")
def test_zx_loan_success():
    with allure.step("数据初始化"):
        id_no, birthday = get_zx_user_id_no()
        user_name = get_user_name()
        mobile_no = get_phone_mum()
        acct_no = get_ccb_num()
        custid = get_cust_id()
        bank_name = "中国建设银行"
        loan_amt = "2000"
        reqPeriods = "12"

        loan_sqe_no = get_req_seq_no()
        req_no = get_req_no()
        bk_no = get_bank_id()
        fk_no = get_fk_id()
        logging = Logger().init_logger()

    with allure.step("发起授信/客户信息同步"):
        # 1.授信申请加密
        sx_need_encry_data = {'apiKey': 'ZLSK-ZX', 'params':json_dumps_cn({"birthday":birthday,"applyDt":"2024-07-04","maxDegree":"10","maritalStatus":"10","idStartDate":"2024-07-18","signOffice":"罗定市公安局","mobileNo":mobile_no,"gender":"F","userName":user_name,"loanseqno":loan_sqe_no,"idNo":id_no,"monthlySalary":"1000","idExpireDate":"9999-12-31","custId":custid,"fromChannel":"01","fileIDs":"a8c06a83a1554ecca27faceb1ed92f5a1689327582151,86a039f4527440bb905fc47ca51a78a31689327582552,a963544b648143f19fd57f79405109511689327582670,7f485a58bc7e492f8bba988d7fd1f2561689327582760,1b1125bd7bdd42e29930b5a64e06c6aa1689327582873,fcf14e96ee7e4dd5a0d747d9683eb1201689327582970,10e462213a5c407cacf2b23dc8933af41689327583096,afc5eea447464782a47f12462b16a60c1689327583885","regAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"liveAddress":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"emergencyContact":[{"relation":"01","mobileNo":"18197269653","name":"毛不易"},{"relation":"02","mobileNo":"18197269659","name":"李文忠"}],"occupationInfo":{"companyAddInfo":{"area":"440106","address":"广东省广州市天河区冼村街道珠江东路11号","province":"440000","city":"440100"},"profession":"0","companyPhone":"02035949111","companyName":"测试科技有限公司","industry":"A","position":"01"},"loanInfo":{"priceAcc":"0.2395","loanFreq":"1M","rateType":"1","loanType":"PZ","reqPeriods":reqPeriods,"reqAmount":loan_amt,"dueDayOpt":"1","custDayRate":"0.2395","reqPurpose":"1"},"accInfoList":[{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"},{"acctKind":"02","acctTyp":"01","acctBankCode":"0105","bankName":bank_name,"acctNo":acct_no,"acctName":user_name,"idNo":id_no,"acctPhone":mobile_no,"phoneBelongAddr":"云浮"}]}), 'requestNo': req_no}
        # 加密数据
        sx_encry_data = encrypt_decrypt().param_encry_by_channel(sx_need_encry_data, 'zhenXing')
        # 1.授信申请请求,获取返回数据
        sxsq_resp = core_zjly_api().test_order_apply(sx_encry_data)
        # 1.授信申请返回数据解密
        decry_data = encrypt_decrypt().param_decrys_by_channel(sxsq_resp, 'zhenXing')
        logging.info(f"解密后的授信申请返回数据为：======{decry_data}")

    with allure.step("授信状态查询"):
        # 2.授信状态查询加密
        zt_need_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的授信状态查询数据为：======{zt_need_ency_data}")
        sxzt_encry = encrypt_decrypt().param_encry_by_channel(zt_need_ency_data,'zhenXing')
        logging.info(f"加密后的授信状态查询数据为：======{sxzt_encry}")
        # 轮训读取判断查询结果，为"授信通过"则跳出
        # 2.授信状态查询请求
        loop_result().loop_sxcx_result(sxzt_encry,'zhenXing')

    with allure.step("发起通联绑卡"):
        # 3.签约申请加密
        qybk_ency_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"seqno":bk_no,"loanseqno":loan_sqe_no,"id_no":id_no,"user_name":user_name,"mobile_no":mobile_no,"bankCode":"0105","cardNo":acct_no,"bankName":bank_name,"registerPhone":mobile_no}),"requestNo": req_no}
        # 加密数据
        logging.info(f"需要加密的签约申请数据为：======{qybk_ency_data}")
        qybk_encry = encrypt_decrypt().param_encry_by_channel(qybk_ency_data, 'zhenXing')
        logging.info(f"加密后的签约申请数据为：======{qybk_encry}")
        # 3.签约申请请求
        qysq_resp = core_zjly_api().test_binding_card_apply(qybk_encry)
        # 3.签约申请返回数据解密
        qysq_decry = encrypt_decrypt().param_decrys_by_channel(qysq_resp,'zhenXing')
        logging.info(f"解密后的签约申请返回数据为：======{qysq_decry}")

    with allure.step("绑卡签约确认"):
        # 4.签约确认加密
        qyqr_encry_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"seqno":bk_no,"smscode":"111111"}),"requestNo": req_no}
        # 需要将数据再次格式化成带转义符并且去除空格
        qyqr_encry = encrypt_decrypt().param_encry_by_channel(qyqr_encry_data,'zhenXing')
        logging.info(f"加密后的签约确认数据为：======{qyqr_encry}")
        # 4.签约确认请求
        qyqr_resp = core_zjly_api().test_binding_card_confirm(qyqr_encry)
        # 4.签约确认返回数据解密
        qyqr_decry = encrypt_decrypt().param_decrys_by_channel(qyqr_resp,'zhenXing')
        logging.info(f"解密后的签约确认返回数据为：======{qyqr_decry}")

    with allure.step("发起借款"):
        # 5.放款申请加密
        fk_encry_data = {"apiKey":"ZLSK-ZX","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no,"amt":loan_amt,"fileIDs":"1780487717038329856,6b2a97dc90794fe2b78fa5412c82be581713337050255","accInfoDto":{"acctKind":"01","acctTyp":"01","acctBankCode":"0105","acct_no":acct_no,"acctName":user_name,"id_no":id_no,"acctPhone":mobile_no,"bankName":bank_name}}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的放款申请数据为：======{fk_encry_data}")
        fksq_encry = encrypt_decrypt().param_encry_by_channel(fk_encry_data, 'zhenXing')
        logging.info(f"加密后的放款申请数据为：======{fksq_encry}")
        # 5.放款申请请求
        fksq_resp = core_zjly_api().test_loan_apply_settle(fksq_encry)
        # 5.放款申请返回数据解密
        fksq_decry = encrypt_decrypt().param_decrys_by_channel(fksq_resp, 'zhenXing')
        logging.info(f"解密后的放款申请返回数据为：======{fksq_decry}")

    with allure.step("借款状态查询"):
        # 6.放款状态查询加密
        fkzt_encry_data = {"apiKey": "ZLSK-ZX","params":json_dumps_cn({"requestNo":fk_no,"loanseqno":loan_sqe_no}),"requestNo": req_no}
        # 加密数据
        fkzt_encry = encrypt_decrypt().param_encry_by_channel(fkzt_encry_data, 'zhenXing')
        logging.info(f"加密后的放款状态数据为：======{fkzt_encry}")
        # 轮询查询放款结果，查询到结果为"放款成功"则跳出
        # 6.放款状态查询请求
        loop_result().loop_fkcx_result(fkzt_encry, 'zhenXing')

    with allure.step("还款计划查询"):
        # 放款成功后需要再次调用一下还款计划接口，落库更新
        # 7.还款计划查询加密
        hkjh_encry_data = {"apiKey":"ZLSK-ZX","params":json_dumps_cn({"loanseqno":loan_sqe_no}),"requestNo":req_no}
        # 加密数据
        logging.info(f"需要加密的还款计划查询数据为：======{hkjh_encry_data}")
        hkjh_encry = encrypt_decrypt().param_encry_by_channel(hkjh_encry_data, 'zhenXing')
        logging.info(f"加密后的还款计划查询数据为：======{hkjh_encry}")
        # 7.还款计划查询请求
        hkjh_resp = core_zjly_api().test_loan_apply_order_query(hkjh_encry)
        # 7.还款计划查询返回数据解密
        hkjh_decry = encrypt_decrypt().param_decrys_by_channel(hkjh_resp, 'zhenXing')
        logging.info(f"解密后的还款计划查询数据为：======{hkjh_decry}")
    #
    # with allure.step("断言绑卡信息表"):
    #     banding_card_success_assert(bk_no, banding_card_assert_data)
    #
    # with allure.step("断言授信订单表"):
    #     loan_success_assert(loan_sqe_no, loan_success_assert_data)
